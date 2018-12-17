from ..exceptions import IllegalArgumentError
from typing import Type


class TypeDict(dict):
    def __init__(self, key_type: Type,  value_type: Type=None):
        self._key_type = key_type
        self._value_type = value_type or object

    def __getitem__(self, k):
        return super(TypeDict, self).__getitem__(self._ensure_type(k, self._key_type))

    def __setitem__(self, k, v):
        return super(TypeDict, self).__setitem__(self._ensure_type(k, self._key_type), self._ensure_type(v, self._value_type))

    def __delitem__(self, k):
        return super(TypeDict, self).__delitem__(self._ensure_type(k, self._key_type))

    def get(self, k, default=None):
        raise NotImplementedError("Method get is not implemented in TypeDict.")

    def setdefault(self, k, default=None):
        raise NotImplementedError(
            "Method setdefault is not implemented in TypeDict.")

    def __contains__(self, k):
        return super(TypeDict, self).__contains__(self._ensure_type(k, self._key_type))

    def _ensure_type(self, obj, type):
        if not isinstance(obj, type):
            raise IllegalArgumentError(
                "Given object {object} is not a {type} object.".format(type=type.__name__, object=obj))
        return obj
