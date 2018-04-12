import pickle
import os
from patricia import trie
import time

class Trie:
    def __init__(self):
        self._trie = trie()

    def __contains__(self,value):
        return value in self._trie

    def __len__(self):
        return len(self._trie)

    def add(self,el):
        """Adds an element to the trie"""
        self._trie[el] = None
