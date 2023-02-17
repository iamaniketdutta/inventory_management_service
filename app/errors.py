from enum import Enum


class ActivityErrorCodes(Enum):
    ACTIVITY_MISCONFIGURED_ATTRIBUTE = (
        "Activity is not configured well, missing attribute {attribute_name}"
    )
