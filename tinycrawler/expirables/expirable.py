from collections import ChainMap
from ..collections import Usable
import json
from ..exceptions import ExpiredError, IllegalArgumentError


class Expirable(Usable):

    def __init__(self, **kwargs):
        """Creates an expirable object, an object which when either is used, or causes a number of errors, is no longer available.
            maximum_consecutive_errors:int, maximum number of consecutive errors before object expires.
            maximum_error_threshold:float, maximum threshold of error/attempts before the object expires.
        """
        super(Expirable, self).__init__(**kwargs)
        self._maximum_consecutive_errors = kwargs.get(
            "maximum_consecutive_errors",
            -1
        )
        self._maximum_error_rate = kwargs.get(
            "maximum_error_threshold",
            1
        )

        if self._maximum_error_rate <= 0:
            raise IllegalArgumentError(
                "Given `maximum_error_threshold` is equal or less than 0. Provide a value greater than zero.")

        if self._maximum_error_rate > 1:
            raise IllegalArgumentError(
                "Given `maximum_error_threshold` is greater than 1. Provide a value lesser than one.")

        self._errors = self._usages = self._consecutive_errors = 0

    @property
    def _error_rate(self)->float:
        if self._usages:
            return self._errors / self._usages
        return 0

    @property
    def expired(self) -> bool:
        """Return boolean representing if given object has expired."""
        return self._error_rate >= self._maximum_error_rate and (self._consecutive_errors >= self._maximum_consecutive_errors or self._maximum_consecutive_errors == -1)

    def used(self, **kwargs):
        """Add results of last usage to class error counter.
            success:bool, represents status of last usage.
        """
        super(Expirable, self).used()
        self._errors += not kwargs["success"]
        self._usages += 1
        if kwargs["success"]:
            self._consecutive_errors = 0
        else:
            self._consecutive_errors += 1

    def use(self):
        """Raise `ExpiredError` if object has expired."""
        if self.expired:
            raise ExpiredError()

    def __repr__(self):
        return {
            "usages": self._usages,
            "errors": self._errors,
            "consecutive_errors": self._consecutive_errors,
            "error_rate": self._error_rate,
            "maximum_error_rate": self._maximum_error_rate,
            "maximum_consecutive_errors": self._maximum_consecutive_errors,
            "expired": self.expired
        }

    def __str__(self):
        return json.dumps(self.__repr__(), indent=4)
