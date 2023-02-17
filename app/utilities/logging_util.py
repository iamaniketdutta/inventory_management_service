from logging import INFO, Formatter, StreamHandler, getLogger
from sys import stdout

from flask import has_request_context, request
from utilities.singleton_utils import Singleton


class RequestFormatter(Formatter):
    def format(self, record):
        record.request_id = ""
        if has_request_context():
            record.request_id = request.id
        return super().format(record)


class LOGSetup(metaclass=Singleton):
    """log setup with configuration"""

    def __init__(self):
        # create logger
        self._logger = getLogger()
        self._logger.setLevel(INFO)

        formatter = RequestFormatter(
            "[%(asctime)s] [%(thread)d] [%(request_id)s] [%(levelname)s] "
            "[%(filename)s] [%(funcName)s:%(lineno)d] : %(message)s"
        )

        # create console handler
        handler = StreamHandler(stdout)
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def get_logger(self):
        return self._logger


logger = LOGSetup().get_logger()
