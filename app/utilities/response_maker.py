import datetime

import simplejson
from flask import Response, request
from utilities import http_status


class GenericJsonEncoder(simplejson.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.time) or isinstance(o, datetime.datetime):
            return o.isoformat()
        return super(GenericJsonEncoder, self).default(o)


class MakeResponse:
    @staticmethod
    def send_response(response_object, status_code):
        return Response(
            response=simplejson.dumps(
                response_object, separators=(",", ":"), cls=GenericJsonEncoder
            ),
            status=status_code,
            mimetype="application/json",
        )

    @staticmethod
    def error(
        error_message, error_code=http_status.HTTP_400_BAD_REQUEST, request_id=""
    ):
        error = {
            "error_message": f"{error_message}",
            "success": False,
            "request_id": request_id if request_id else request.id,
        }
        return MakeResponse.send_response(error, error_code)
