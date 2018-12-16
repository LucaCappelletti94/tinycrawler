from collections import ChainMap
from ..collections import Usable
import json
from ..exceptions import IllegalArgumentError


class Expirable(Usable):

    def __init__(self, **kwargs):
        """Creates an expirable object, an object which when either is used, or causes a number of errors, is no longer available.
            maximum_consecutive_errors:int, maximum number of consecutive errors before object expires.
            maximum_error_rate:float, maximum threshold of error/attempts before the object expires.
        """
        super(Expirable, self).__init__(**kwargs)

        self._errors = self._total_usages = self._consecutive_errors = 0

        self._maximum_consecutive_errors = kwargs.get(
            "maximum_consecutive_errors",
            -1
        )
        self._maximum_error_rate = kwargs.get(
            "maximum_error_rate",
            1
        )

        if self._maximum_error_rate <= 0:
            raise IllegalArgumentError(
                "Given `maximum_error_rate` is equal or less than 0. Provide a value greater than zero.")

        if self._maximum_error_rate > 1:
            raise IllegalArgumentError(
                "Given `maximum_error_rate` is greater than 1. Provide a value lesser than one.")

        if self._maximum_consecutive_errors < -1:
            raise IllegalArgumentError(
                "Given `maximum_consecutive_errors` is smaller than -1. Provide positive integer or -1 for don't care.")

        if (self._maximum_error_rate < 1) != (self._maximum_consecutive_errors != -1):
            raise IllegalArgumentError(
                "Expirable: Either provide two active constraint or None.")

    @property
    def _error_rate(self)->float:
        if self._total_usages:
            return self._errors / self._total_usages
        return 0

    def is_available(self) -> bool:
        """Return boolean representing if given object has expired."""
        return self._error_rate <= self._maximum_error_rate or (self._consecutive_errors < self._maximum_consecutive_errors and self._maximum_consecutive_errors != -1)

    def used(self, **kwargs):
        """Add results of last usage to class error counter.
            success:bool, represents status of last usage.
        """
        super(Expirable, self).used(**kwargs)
        self._errors += not kwargs["success"]
        self._total_usages += 1
        if kwargs["success"]:
            self._consecutive_errors = 0
        else:
            self._consecutive_errors += 1

    def use(self, **kwargs):
        """Raise `ExpiredError` if object has expired."""
        super(Expirable, self).use(**kwargs)

    def ___repr___(self):
        return {
            **super(Expirable, self).___repr___(),
            **{
                "total_usages": self._total_usages,
                "total_errors": self._errors,
                "consecutive_errors": self._consecutive_errors,
                "error_rate": self._error_rate,
                "maximum_error_rate": self._maximum_error_rate,
                "maximum_consecutive_errors": self._maximum_consecutive_errors,
                "expired": not Expirable.is_available(self)
            }}
