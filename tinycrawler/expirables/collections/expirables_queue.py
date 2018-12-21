from ...collections import TypeList
from ...exceptions import IllegalArgumentError
from ..expirable import Expirable
from typing import Type
from queue import Empty
from ...utils import Printable


class ExpirablesQueue(TypeList, Printable):
    def __init__(self, expirable_type: Type, *args, **kwargs):
        super(ExpirablesQueue, self).__init__(
            expirable_type, *args, **kwargs)

        if not issubclass(expirable_type, Expirable):
            raise IllegalArgumentError(
                "Given type {type} is not a subclass of Expirable".format(
                    type=expirable_type.__name__
                ))

    def empty(self, **kwargs)->bool:
        return not self or not self[0].is_available(**kwargs)

    def pop(self, **kwargs):
        if self.empty(**kwargs):
            raise Empty
        return super(ExpirablesQueue, self).pop(0)

    def add(self, expirable: Expirable, **kwargs):
        if expirable.expired:
            raise IllegalArgumentError(
                "Given expirable {expirable} is already expired!".format(
                    expirable=expirable
                ))
        if expirable.is_available(**kwargs):
            super(ExpirablesQueue, self).prepend(expirable)
        else:
            super(ExpirablesQueue, self).append(expirable)

    def ___repr___(self):
        return [
            value.___repr___() for value in self
        ]
