"""Client side wrapper to avoid Pipe breaking on Empty exception, yet still transfer the exception info."""
from .queue_wrapper import QueueWrapper
from queue import Empty
from typing import Dict


class ClientQueueWrapper(QueueWrapper):
    """Client side wrapper to avoid Pipe breaking on Empty exception, yet still transfer the exception info."""

    def add(self, element, *args, **kwargs):
        self._queue.add(element, *args, **kwargs)

    def pop(self, *args, **kwargs):
        value = self._queue.pop(*args, **kwargs)
        if value is None:
            raise Empty
        return value

    def ___repr___(self)->Dict:
        return self._queue.visualize()
