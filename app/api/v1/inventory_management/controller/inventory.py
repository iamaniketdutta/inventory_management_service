from api.v1.inventory_management.activities.get_inventory import GetInventory
from api.v1.inventory_management.schema.inventory_schema import (
    GetQueryModel,
    SuccessResponseGet,
)
from flask import request
from flask_pydantic import validate
from flask_restful import Resource
from utilities.decorators import format_pydantic_error
from utilities.exceptions import ApiException, InvalidPayloadException
from utilities.http_status import HTTP_500_INTERNAL_SERVER_ERROR
from utilities.logging_util import logger
from utilities.response_maker import MakeResponse


class Inventory(Resource):
    @format_pydantic_error
    @validate()
    def get(self, query: GetQueryModel):
        try:
            filter = request.get_json() if request.is_json else {}
            logger.info(f"GetInventory Payload: {query}, {filter}")
            return SuccessResponseGet(
                data=GetInventory().execute(query, filter=filter), request_id=request.id
            )
        except InvalidPayloadException as ie:
            logger.info(
                "GetInventory InvalidPayloadException raised. "
                f"Payload: {query}, {filter} || Error: {ie.message}"
            )
            return MakeResponse.error(ie.message, error_code=ie.status_code)
        except ApiException as e:
            logger.error(
                "GetInventory Api Exception "
                f"error: {e.message} || Payload: {query}, {filter}"
            )
            return MakeResponse.error(error_message=e.message, error_code=e.status_code)
        except Exception as e:
            logger.exception(
                f"GetInventory Exception error: {e} || Payload: {query}, {filter}"
            )
            return MakeResponse.error(
                error_message=str(e), error_code=HTTP_500_INTERNAL_SERVER_ERROR
            )
