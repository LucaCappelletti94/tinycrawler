from .usable import Usable
from ..exceptions import InUseError, NotInUseError
import json


class Sequential(Usable):
    def __init__(self, **kwargs):
        """Define an usable object with a maximum parallel usage.
            maximum_usages:int, maximum parallel usages.
        """

        super(Sequential, self).__init__(**kwargs)
        self._maximum_usages = kwargs.get("maximum_usages", -1)
        self._parallel_usages = 0

    def is_available(self):
        return self._parallel_usages < self._maximum_usages or self._maximum_usages == -1

    def use(self, **kwargs):
        super(Sequential, self).use(**kwargs)
        if not Sequential.is_available(self):
            raise InUseError()
        self._parallel_usages += 1

    def used(self, **kwargs):
        super(Sequential, self).used(**kwargs)
        if self._parallel_usages == 0:
            raise NotInUseError()
        self._parallel_usages -= 1

    def _constraints_are_active(self)->bool:
        """Return a boolean representing if constraints are active."""
        return self._maximum_usages != -1

    def ___repr___(self):
        return {
            "maximum_usages": self._maximum_usages,
            "parallel_usages": self._parallel_usages,
            "sequential_is_available": Sequential.is_available(self)
        }
