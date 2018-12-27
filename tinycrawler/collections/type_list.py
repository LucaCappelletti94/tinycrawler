"""Create a list which raises an assertion error when type does not match with given one."""
from typing import Type, Dict
from ..utils import Printable


class TypeList(list, Printable):
    """Create a list which raises an assertion error when type does not match with given one."""

    def __init__(self, list_type: Type):
        """Create a list which raises an assertion error when type does not match with given one."""
        super(TypeList, self).__init__()
        self._type = list_type

    @property
    def type(self)->Type:
        """Return list type."""
        return self._type

    def __setitem__(self, index, value):
        """Disable direct setting of an element in list."""
        raise NotImplementedError("Set item is not available in TypeList.")

    def append(self, value):
        """Append given value to the bottom of list."""
        super(TypeList, self).append(self._ensure_type(value))

    def prepend(self, value):
        """Append given value to the head of list."""
        super(TypeList, self).insert(0, self._ensure_type(value))

    def _ensure_type(self, key):
        """Verify that given object has the correct type."""
        assert isinstance(key, self._type)
        return key

    def ___repr___(self)->Dict:
        """Return a dictionary representing the object."""
        return {
            "type": self._type.__name__
        }
