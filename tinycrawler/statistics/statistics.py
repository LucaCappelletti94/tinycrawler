import time
from collections import defaultdict
from datetime import datetime, timedelta
from multiprocessing import Lock


class Statistics(dict):
    def __init__(self):
        self._lock = Lock()

    def add(self, category: str, name: str, value: int=1):
        """Add value to category/name and updates total."""
        self._lock.acquire()
        if category not in self:
            self[category] = defaultdict(int)

        self[category][name] += value
        self._lock.release()

    def set(self, category: str, name: str, value: int=1):
        """Add value to category/name and updates total."""
        self._lock.acquire()
        if category not in self:
            self[category] = defaultdict(int)

        self[category][name] = value
        self._lock.release()

    def keys(self):
        return super().keys()

    def get(self, key):
        return super().__getitem__(key)
