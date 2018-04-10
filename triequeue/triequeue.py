import queue
from .trie.trie import Trie

class triequeue(queue.Queue):

    def __init__(self):
        super().__init__()
        self._trie = Trie()

    def get(self, block=True, timeout = None):
        return super().get(block = block, timeout = timeout)

    def put(self, element):
        super().put(element)
        self._trie.add(element)

    def contains(self, value):
        return value in self._trie