"""Create sporadically available object."""
from .usable import Usable
from ..exceptions import IllegalArgumentError
from time import time


class Sporadic(Usable):
    """Create sporadically available object."""

    def __init__(self, **kwargs):
        """Create sporadically available object.
            use_timeout:float, unavailability timeout after use.
            used_timeout:float, unavailability timeout after used.
        """

        super(Sporadic, self).__init__(**kwargs)
        self._set_available_time()
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
                "Given `use_timeout` is less than 0. Provide a value >= zero.")

        if self._used_timeout < 0:
            raise IllegalArgumentError(
                "Given `used_timeout` is less than 0. Provide a value >= to zero.")

    def is_available(self, **kwargs)->bool:
        """Determine if sporadic object is now available."""
        return time() >= self._available_time

    def _set_available_time(self, timeout: float = 0):
        self._available_time = time() + timeout

    def use(self, **kwargs):
        """Update next available timeout using the `use` timeout."""
        super(Sporadic, self).use(**kwargs)
        self._set_available_time(self._use_timeout)

    def used(self, **kwargs):
        """Update next available timeout using the `used` timeout."""
        super(Sporadic, self).used(**kwargs)
        self._set_available_time(self._used_timeout)

    def ___repr___(self):
        """Return a dictionary representing the object."""
        return {
            **super(Sporadic, self).___repr___(),
            **{
                "use_timeout": self._use_timeout,
                "used_timeout": self._used_timeout,
                "sporadic_is_available": Sporadic.is_available(self)
            }}
