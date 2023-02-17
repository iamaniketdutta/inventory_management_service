import errors
from utilities.http_status import HTTP_400_BAD_REQUEST


class ExceptionBase(Exception):
    status_code = HTTP_400_BAD_REQUEST

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        if status_code is not None:
            self.status_code = status_code

        if message is not None:
            self.message = message

    def __str__(self) -> str:
        return self.message

    @property
    def status(self):
        return self.status_code

    @property
    def data(self):
        error = {"message": self.message, "error_code": self.status_code}
        return {"error": error, "success": False}


class ApiException(ExceptionBase):
    status_code = HTTP_400_BAD_REQUEST
    message = "Api Exception raised"


class ActivityMisConfigured(ExceptionBase):
    """Will be raised when there is some missing configuration
    in the activity defined being inherited from base."""

    error_class = errors.ActivityErrorCodes


class InvalidPayloadException(ExceptionBase):
    status_code = HTTP_400_BAD_REQUEST
    message = "Invalid payload"
