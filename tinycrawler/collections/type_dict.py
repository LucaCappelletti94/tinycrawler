from ..exceptions import IllegalArgumentError
from typing import Type


class TypeDict(dict):
    def __init__(self, type: Type, *args, **kwargs):
        self._type = type

    def __getitem__(self, k):
        return super(TypeDict, self).__getitem__(self._ensure_type(k))

    def __setitem__(self, k, v):
        return super(TypeDict, self).__setitem__(self._ensure_type(k), v)

    def __delitem__(self, k):
        return super(TypeDict, self).__delitem__(self._ensure_type(k))

    def get(self, k, default=None):
        raise NotImplementedError("Method get is not implemented in TypeDict.")

    def setdefault(self, k, default=None):
        raise NotImplementedError(
            "Method setdefault is not implemented in TypeDict.")

    def __contains__(self, k):
        return super(TypeDict, self).__contains__(self._ensure_type(k))

    def _ensure_type(self, key):
        if not isinstance(key, self._type):
            raise IllegalArgumentError(
                "Given key is not a {type} object.".format(type=self._type.__name__))
        return key
