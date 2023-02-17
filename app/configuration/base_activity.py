from abc import ABC, abstractmethod

from flask import request
from utilities.exceptions import ActivityMisConfigured


class ActivityBase(ABC):
    """
    Base class for all the activities,
    defining the sequence of execution and controlling the
    validations and response structures.
    """

    context_class = None
    """Holds the reference to the context object class"""

    def __init__(self, request_id="", *args, **kwargs):
        """
        Initializing the response and other objects
        Note - If any other attribute is to be added in the instance
         then override this and call super().__init__()
        """
        self.request_id = request_id if request_id else request.id
        self.context = None
        self.payload = {}

        if not self.context_class:
            raise ActivityMisConfigured(
                "ACTIVITY_MISCONFIGURED_ATTRIBUTE", {"attribute_name": "context_class"}
            )

    def execute(self, payload=None, **kwargs):
        """
        This method controls the sequential execution of each step for the activity.
        Executing the validations first and then the execute part.

        :param payload: Dictionary or Pydantic model consisting of payload
        present in the request directly passed after serialization
        :return:
        """
        response = None
        self.payload = payload if isinstance(payload, dict) else payload.dict()
        # sets the self.context attribute by fetching data from the payload dictionary
        self._set_context(self.payload, **kwargs)

        response = self._execute()

        return response

    def _set_context(self, payload, **kwargs):
        """
        Simply sets the context object as per the payload passed to it
        :param payload:
        :return:
        """
        self.context = self.context_class(**payload)
        if kwargs:
            payload.update(kwargs)
        for name, value in payload.items():
            setattr(self.context, name, value)

    @abstractmethod
    def _execute(self):
        """
        This method needs to be implemented in the inherited
        class only and it will consist of actual
        steps to be performed in the activity.

        And it must also append the data into the response.

        :return:
        """
        raise NotImplementedError("Validate not implemented")
