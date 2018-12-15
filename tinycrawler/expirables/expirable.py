import abc
from ..collections import Usable
from ..exceptions import ExpiredError, IllegalArgumentError


class Expirable(Usable):
    __metaclass__ = abc.ABCMeta

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
        self._maximum_error_threshold = kwargs.get(
            "maximum_error_threshold",
            1
        )

        if self._maximum_error_threshold <= 0:
            raise IllegalArgumentError(
                "Given `maximum_error_threshold` is equal or less than 0. Provide a value greater than zero.")

        if self._maximum_error_threshold > 1:
            raise IllegalArgumentError(
                "Given `maximum_error_threshold` is greater than 1. Provide a value lesser than one.")

        self._errors = self._consecutive_errors = 0

    @property
    def _error_rate(self)->float:
        return self._errors / self._usages

    @property
    def expired(self) -> bool:
        """Return boolean representing if given object has expired."""
        return self._error_rate > self._maximum_error_threshold and self._consecutive_errors > self._maximum_consecutive_errors

    def used(self, **kwargs):
        """Add results of last usage to class error counter.
            success:bool, represents status of last usage.
        """
        super(Expirable, self).used()
        self._errors += not kwargs["success"]

    def use(self):
        """Raise `ExpiredError` if object has expired."""
        if self.expired:
            raise ExpiredError()
