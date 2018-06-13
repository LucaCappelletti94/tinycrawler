import queue


class DictQueue(queue.Queue):

    def __init__(self):
        super().__init__()
        self._data = {}

    def get(self, block=True, timeout=None):
        return super().get(block=block, timeout=timeout)

    def put(self, element):
        super().put(element)
        self._data[element] = None

    def contains(self, value):
        return value in self._data
