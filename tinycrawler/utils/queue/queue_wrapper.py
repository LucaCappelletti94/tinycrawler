from ..output import Printable


class QueueWrapper(Printable):
    def __init__(self, queue):
        self._queue = queue
