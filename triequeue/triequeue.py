from multiprocessing import Queue
from .trie.trie import Trie

class TrieQueue(Queue):

    def __init__(self):
        super().__init__()
        self._trie = Trie()

    def get(self, block=True, timeout = None):
        return super().get(block = block, timeout = timeout)

    def put(self, element):
        super().put(element)
        self._trie.add(url)

    def __contains__(self, element):
        return element in self._trie