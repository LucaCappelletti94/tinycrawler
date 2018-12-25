"""Create a dict which raises an assertion error when type does not match with given ones."""
from typing import Type, Dict
from ..utils import Printable


class TypeDict(dict, Printable):
    """Create a dict which raises an assertion error when type does not match with given ones."""

    def __init__(self, key_type: Type,  value_type: Type = None):
        """Create a dict which raises an assertion error when type does not match with given ones."""
        super(TypeDict, self).__init__()
        self._key_type = key_type
        self._value_type = value_type or object

    def __getitem__(self, k):
        """Return item at given key checking for type."""
        return super(TypeDict, self).__getitem__(self._ensure_type(k, self._key_type))

    def __setitem__(self, k, v):
        """Set item at given key checking for type."""
        return super(TypeDict, self).__setitem__(self._ensure_type(k, self._key_type), self._ensure_type(v, self._value_type))

    def __delitem__(self, k):
        """Delete item at given key checking for type."""
        return super(TypeDict, self).__delitem__(self._ensure_type(k, self._key_type))

    def get(self, k, default=None):
        """Disable direct setting of an element in dict."""
        raise NotImplementedError("Method get is not implemented in TypeDict.")

    def setdefault(self, k, default=None):
        """Disable direct setting of an element in dict."""
        raise NotImplementedError(
            "Method setdefault is not implemented in TypeDict.")

    def __contains__(self, k):
        """Determine whetever a key is contained checking for type."""
        return super(TypeDict, self).__contains__(self._ensure_type(k, self._key_type))

    def _ensure_type(self, obj, value_type: Type):
        """Verify that given object has the correct type."""
        assert isinstance(obj, value_type)
        return obj

    def ___repr___(self)->Dict:
        """Return a dictionary representing the object."""
        return {
            "key_type": self._key_type.__name__,
            "value_type": self._value_type.__name__
        }
