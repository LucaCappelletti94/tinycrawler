"""Server side wrapper to avoid Pipe breaking on Empty exception, yet still transfer the exception info."""
from .queue_wrapper import QueueWrapper
from queue import Empty
from typing import Dict


class ServerQueueWrapper(QueueWrapper):
    """Server side wrapper to avoid Pipe breaking on Empty exception, yet still transfer the exception info."""

    def add(self, element, *args, **kwargs):
        self._queue.add(element, *args, **kwargs)

    def pop(self, *args, **kwargs):
        try:
            return self._queue.pop(*args, **kwargs)
        except Empty:
            return None

    def visualize(self)->Dict:
        return self._queue.___repr___()

    ___repr___ = visualize
