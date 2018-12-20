from ...collections import TypeList
from ...exceptions import IllegalArgumentError
from ..expirable import Expirable
from typing import Type
from queue import Empty
import json


class ExpirablesQueue(TypeList):
    def __init__(self, expirable_type: Type, *args, **kwargs):
        super(ExpirablesQueue, self).__init__(
            expirable_type, *args, **kwargs)

        if not issubclass(expirable_type, Expirable):
            raise IllegalArgumentError("Given type {type} is not a subclass of Expirable".format(
                type=expirable_type.__name__))

    @property
    def empty(self)->bool:
        return not self or not self[0].is_available()

    def pop(self):
        if self.empty:
            raise Empty
        return super(ExpirablesQueue, self).pop(0)

    def add(self, expirable: Expirable):
        if expirable.expired:
            raise IllegalArgumentError(
                "Given expirable {expirable} is already expired!".format(expirable=expirable))
        if expirable.is_available():
            super(ExpirablesQueue, self).prepend(expirable)
        else:
            super(ExpirablesQueue, self).append(expirable)

    def ___repr___(self):
        return [
            value.___repr___() for value in self
        ]

    def __repr__(self):
        return json.dumps(self.___repr___(), indent=4, sort_keys=True)

    __str__ = __repr__
