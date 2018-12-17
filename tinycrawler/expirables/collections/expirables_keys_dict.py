from ...collections import TypeDict
from collections import OrderedDict
from ...exceptions import IllegalArgumentError, UnavailableError
from ..expirable import Expirable
from typing import Type


class ExpirableKeysDict(TypeDict):
    def __init__(self, expirable_type: Type, *args, **kwargs):
        super(ExpirableKeysDict, self).__init__(
            expirable_type, *args, **kwargs)

        if not issubclass(expirable_type, Expirable):
            raise IllegalArgumentError("Given type {type} is not a subclass of Expirable".format(
                type=expirable_type.__name__))

        self._keys = OrderedDict()

    def __getitem__(self, k):
        self._keys[k].use()
        return super(ExpirableKeysDict, self).__getitem__(self._ensure_availability(k))

    def __setitem__(self, k, v):
        self._keys[k] = k
        return super(ExpirableKeysDict, self).__setitem__(self._ensure_availability(k), v)

    def __delitem__(self, k):
        del self._keys[k]
        return super(ExpirableKeysDict, self).__delitem__(k)

    def used(self, k, **kwargs):
        self._keys[k].used(**kwargs)

    def is_available(self, k):
        return (k in self and self._keys[k].is_available()) or (k not in self and k.is_available())

    def _ensure_availability(self, key):
        if not self.is_available(key):
            raise UnavailableError()
        return key
