"""Create a dict which raises an assertion error when type does not match with given ones or isn't a subclass of Expirable."""
from ...collections import TypeDict
from ..expirable import Expirable
from typing import Type


class ExpirableKeysDict(TypeDict):
    """Create a dict which raises an assertion error when type does not match with given ones or isn't a subclass of Expirable."""

    def __init__(self, expirable_type: Type, other: Type):
        """Create a dict which raises an assertion error when type does not match with given ones or isn't a subclass of Expirable."""
        super(ExpirableKeysDict, self).__init__(expirable_type, other)
        assert issubclass(expirable_type, Expirable)
        self._expirables = TypeDict(expirable_type, expirable_type)

    def __getitem__(self, expirable: Expirable):
        """Return item at given key checking for type and availability."""
        return super(ExpirableKeysDict, self).__getitem__(
            self._ensure_availability(expirable)
        )

    def __setitem__(self, expirable: Expirable, v):
        """Set item at given key checking for type and availability."""
        if expirable not in self._expirables:
            self._expirables[expirable] = expirable
        return super(ExpirableKeysDict, self).__setitem__(
            self._ensure_availability(expirable), v
        )

    def __delitem__(self, expirable: Expirable):
        """Delete item at given key checking for type and eliminating key from list too."""
        del self._expirables[expirable]
        return super(ExpirableKeysDict, self).__delitem__(expirable)

    def used(self, expirable: Expirable, **kwargs):
        """Call `used` on given key expirable object."""
        self._expirables[expirable].used(**kwargs)

    def use(self, expirable: Expirable, **kwargs):
        """Call `use` on given key expirable object."""
        self._expirables[expirable].use(**kwargs)

    def is_available(self, e: Expirable, **kwargs)->bool:
        """Return boolean representing if given object is available for use."""
        return (
            e in self and self._expirables[e].is_available(**kwargs)
        ) or (
            e not in self and e.is_available(**kwargs)
        )

    def _ensure_availability(self, expirable: Expirable)->Expirable:
        """Raise AssertionError if given object is not available."""
        assert self.is_available(expirable)
        return expirable
