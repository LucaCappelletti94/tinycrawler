"""Define an usable object with a maximum parallel usage."""
from .usable import Usable
from ..exceptions import NotInUseError


class Sequential(Usable):
    """Define an usable object with a maximum parallel usage."""

    def __init__(self, **kwargs):
        """Define an usable object with a maximum parallel usage.
            maximum_usages:int, maximum parallel usages.
        """
        super(Sequential, self).__init__(**kwargs)
        self._maximum_usages = kwargs.get("maximum_usages", -1)
        self._parallel_usages = 0

    def is_available(self, **kwargs)->bool:
        """Determine if object is at maximum parallel usages."""
        return self._parallel_usages < self._maximum_usages or self._maximum_usages == -1

    def use(self, **kwargs):
        """Increase parallel usages by one."""
        super(Sequential, self).use(**kwargs)
        self._parallel_usages += 1

    def used(self, **kwargs):
        """Decrease parallel usages by one. Throws an exception if the usages are already zero."""
        super(Sequential, self).used(**kwargs)
        if self._parallel_usages == 0:
            raise NotInUseError()
        self._parallel_usages -= 1

    def ___repr___(self)->dict:
        """Return a dictionary representation of object."""
        return {
            "maximum_usages": self._maximum_usages,
            "parallel_usages": self._parallel_usages,
            "sequential_is_available": Sequential.is_available(self)
        }
