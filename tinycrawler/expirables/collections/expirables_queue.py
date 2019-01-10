"""Create a queue which raises an assertion error when type does not match with given one."""
from ..expirable import Expirable
from typing import Dict
from queue import Empty


class ExpirablesQueue:
    """Create a queue which raises an assertion error when type does not match with given one."""

    def __init__(self):
        """Create a queue which raises an assertion error when type does not match with given one."""
        self._expirables = []

    def empty(self, **kwargs)->bool:
        """Determine if there is an available element in the queue."""
        return not self or not self._expirables[-1].is_available(**kwargs)

    def pop(self, **kwargs)->Expirable:
        """Return first available element of queue."""
        if self.empty(**kwargs):
            raise Empty
        return self._expirables.pop()

    def add(self, expirable: Expirable, **kwargs):
        """Add given expirable element to list, if available is put on top, else to bottom."""
        assert not expirable.expired
        if expirable.is_available(**kwargs):
            self._expirables.append(expirable)
        else:
            self._expirables.insert(0, expirable)

    def ___repr___(self)->Dict:
        """Return a dictionary representation of object."""
        return [
            value.___repr___() for value in self._expirables
        ]
