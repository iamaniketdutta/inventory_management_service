from functools import wraps

from utilities.http_status import HTTP_400_BAD_REQUEST
from utilities.logging_util import logger
from utilities.operation_utils import join_after_typecast
from utilities.response_maker import MakeResponse


def format_pydantic_error(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        res = fn(*args, **kwargs)
        err_json = res.get_json()
        # check if pydantic throws an error (if not continue normally)
        if (err_json is None) or ("validation_error" not in err_json):
            return res
        val_err: dict = err_json["validation_error"]
        final_msg: str = ""
        for param_type in val_err.keys():
            for single_error in val_err[param_type]:
                final_msg += (
                    f"{ join_after_typecast(single_error.get('loc', [])) }:"
                    f" {single_error.get('msg')}, "
                )
        logger.info(final_msg)
        return MakeResponse.error(
            error_message=final_msg.strip(", "),
            error_code=HTTP_400_BAD_REQUEST,
        )

    return wrapper
