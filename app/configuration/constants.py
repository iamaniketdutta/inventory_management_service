from enum import Enum


class Common(Enum):
    VERSION = "1"
    COUNT = "count"
    DATA = "data"


class Numeric(Enum):
    ZERO = 0
    ONE = 1
    TWENTY = 20


class HeaderConstants(Enum):
    AUTHORIZATION = "Authorization"
