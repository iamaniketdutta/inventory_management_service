#!/usr/bin/python

import traceback
from uuid import uuid4

from configuration.constants import HeaderConstants
from configuration.route import api_v1_bp
from flask import Flask, Response, json, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from simple_settings import settings
from utilities import messages
from utilities.exceptions import ExceptionBase
from utilities.http_status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_503_SERVICE_UNAVAILABLE,
    is_server_error,
)
from utilities.logging_util import logger
from utilities.response_maker import MakeResponse


def init_swagger(app_):
    # swagger specific #
    SWAGGER_URL = "/api/v1/docs"
    API_URL = "/static/swagger.json"
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL, config={"app_name": "inventory_management_service"}
    )
    app_.register_blueprint(SWAGGERUI_BLUEPRINT)
    return app_


def create_app():
    app_ = Flask(__name__)
    env = app_.config["ENV"]
    app_.config.from_object(f"settings.{env}")

    # Register v1 api blueprint
    app_.register_blueprint(api_v1_bp)
    app_ = init_swagger(app_)
    return app_


app = create_app()
cors = CORS(app)


@app.before_request
def authenticate_request():
    request.id = f"{uuid4()}"

    try:
        if (
            any(route in request.path for route in settings.UNPROTECTED_ROUTES)
            or request.method == "OPTIONS"
        ):
            return

        headers = dict(request.headers)
        auth_header = headers.get(HeaderConstants.AUTHORIZATION.value)

        if not auth_header:
            return MakeResponse.error(messages.NO_AUTH_HEADER)

        if auth_header != settings.token:
            return MakeResponse.error(messages.INVALID_USER_TOKEN)

    except Exception as err:
        status_code = (
            err.status_code
            if hasattr(err, "status_code")
            else HTTP_503_SERVICE_UNAVAILABLE
        )
        err_message = err.message if hasattr(err, "message") else err
        log_message = (
            f"{'ERROR' if is_server_error(status_code) else 'DEBUG'} "
            f"while validating user auth_header:{auth_header}, "
            f"status_code:{status_code}, error: {err_message}"
        )
        if is_server_error(status_code):
            logger.error(log_message)
        else:
            logger.debug(log_message)
        return MakeResponse.error(messages.INVALID_AUTH_HEADER, error_code=status_code)


@app.after_request
def allow_origin(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    response.headers.add(
        "Access-Control-Allow-Headers",
        "Content-Type, Authorization, x-auth-status, user-token",
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS,PATCH"
    )
    return response


@app.errorhandler(HTTP_404_NOT_FOUND)
def page_not_found():
    return Response(
        response=json.dumps(
            {"error": messages.NO_SUCH_RESOURCE, "status_code": HTTP_404_NOT_FOUND}
        ),
        status=HTTP_404_NOT_FOUND,
        headers={"Allow": "GET,PUT,POST,DELETE,OPTIONS,PATCH"},
        mimetype="application/json",
    )


@app.errorhandler(ExceptionBase)
def handle_audit_exception(error):
    response = jsonify(error.data)
    response.status_code = HTTP_400_BAD_REQUEST
    return MakeResponse().error(response.message, response.status_code)


@app.errorhandler(Exception)
def handle_internal_server_error(e):
    logger.exception(traceback.format_exc())
    return MakeResponse().error(str(e), HTTP_500_INTERNAL_SERVER_ERROR)


# Just run app defined
if __name__ == "__main__":
    app.run(debug=settings.DEBUG, port=settings.PORT)
