from ..exceptions import IllegalArgumentError
from typing import Type


class TypeList(list):
    def __init__(self, list_type: Type, *args, **kwargs):
        self._type = list_type

    def __setitem__(self, index, value):
        raise NotImplementedError("Set item is not available in TypeList.")

    def append(self, value):
        super(TypeList, self).append(self._ensure_type(value))

    def prepend(self, value):
        super(TypeList, self).insert(0, self._ensure_type(value))

    def _ensure_type(self, key):
        if not isinstance(key, self._type):
            raise IllegalArgumentError(
                "Given key is not a {type} object.".format(
                    type=self._type.__name__
                ))
        return key
