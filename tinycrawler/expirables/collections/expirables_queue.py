"""Create a queue which raises an assertion error when type does not match with given one."""
from ...collections import TypeList
from ..expirable import Expirable
from typing import Type
from queue import Empty
from ...utils import Printable


class ExpirablesQueue(TypeList, Printable):
    """Create a queue which raises an assertion error when type does not match with given one."""

    def __init__(self, expirable_type: Type, **kwargs):
        """Create a queue which raises an assertion error when type does not match with given one."""
        super(ExpirablesQueue, self).__init__(
            expirable_type
        )
        assert issubclass(expirable_type, Expirable)

    def empty(self, **kwargs)->bool:
        """Determine if there is an available element in the queue."""
        return not self or not self[-1].is_available(**kwargs)

    def pop(self, **kwargs)->Expirable:
        """Return first available element of queue."""
        if self.empty(**kwargs):
            raise Empty
        return super(ExpirablesQueue, self).pop()

    def add(self, expirable: Expirable, **kwargs):
        """Add given expirable element to list, if available is put on top, else to bottom."""
        assert not expirable.expired
        if expirable.is_available(**kwargs):
            super(ExpirablesQueue, self).append(expirable)
        else:
            super(ExpirablesQueue, self).prepend(expirable)

    def ___repr___(self):
        """Return a dictionary representation of object."""
        return [
            value.___repr___() for value in self
        ]
