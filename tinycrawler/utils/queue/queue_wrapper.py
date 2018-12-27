from .queue import Queue
from ..output import Printable


class QueueWrapper(Printable):
    def __init__(self, queue: Queue):
        self._queue = queue

    def pop(self, *args, **kwargs):
        raise NotImplementedError(
            "Method `pop` has to be implemented in subclasses of QueueWrapper."
        )
