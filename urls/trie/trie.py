import pickle
import os
from patricia import trie
import time

class Trie:
    def __init__(self,path=None, cache = True, cache_timeout = 100):
        self._path = path
        self._cache = cache
        self._cache_timeout = cache_timeout
        self._trie = trie()
        if self._is_cached():
            self._last_update = os.path.getmtime(self._path)
            self._load_from_cache()
        else:
            self._last_update = time.time()

    def __contains__(self,value):
        return value in self._trie

    def __len__(self):
        return len(self._trie)

    def _is_cache_enabled(self):
        """Checks if a path was given"""
        return self._path != None and self._cache

    def _is_cached(self):
        """Checks if the file was cached to the given path"""
        return self._is_cache_enabled() and os.path.isfile(self._path)

    def _load_from_cache(self):
        """Loads the trie from the given path"""
        with open(self._path,'rb') as f:
            self = pickle.load(f)

    def _save(self):
        """Saves the trie to the given path"""
        if self._is_cache_enabled():
            if self._last_update < time.time() - self._cache_timeout:
                with open(self._path,'wb') as f:
                    pickle.dump(self, f,-1)
            else:
                with open(self._path,'wb') as f:
                    pickle.dump(self, f,-1)
            self._last_update = time.time()

    def add(self,el):
        """Adds an element to the trie"""
        self._trie[el] = None
        self._save()