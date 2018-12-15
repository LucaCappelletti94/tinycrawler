from .usable import Usable
from ..exceptions import IllegalArgumentError, UnavailableError
from time import time


class Sporadic(Usable):
    def __init__(self, **kwargs):
        super(Sporadic, self).__init__(**kwargs)
        self._use_timeout = kwargs.get(
            "use_timeout",
            0
        )

        self._used_timeout = kwargs.get(
            "used_timeout",
            0
        )

        if self._use_timeout < 0:
            raise IllegalArgumentError(
                "Given `use_timeout` is less than 0. Provide a value greater than or equal to zero.")

        if self._used_timeout < 0:
            raise IllegalArgumentError(
                "Given `used_timeout` is less than 0. Provide a value greater than or equal to zero.")

        self._set_available_time()

    @property
    def available(self)->bool:
        return time() >= self._available_time

    def _set_available_time(self, timeout: float=0):
        self._available_time = time() + timeout

    def use(self, **kwargs):
        super(Sporadic, self).use()
        if not self.available:
            raise UnavailableError()
        self._set_available_time(self._use_timeout)

    def used(self, **kwargs):
        super(Sporadic, self).used()
        self._set_available_time(self._used_timeout)
