import time
from collections import defaultdict
from datetime import datetime, timedelta
from multiprocessing import Lock


class Statistics:
    def __init__(self):
        self.info = {}
        self._lock = Lock()

    def add(self, category: str, name: str, value: int=1):
        """Add value to category/name and updates total."""
        self._lock.acquire()
        if category not in self.info:
            self.info[category] = defaultdict(int)

        self.info[category][name] += value
        self._lock.release()

    def set(self, category: str, name: str, value: int=1):
        """Add value to category/name and updates total."""
        self._lock.acquire()
        if category not in self.info:
            self.info[category] = defaultdict(int)

        self.info[category][name] = value
        self._lock.release()

    def remove(self, category: str, name: str, value: int=1):
        """Remove value to category/name."""
        self._lock.acquire()
        self.info[category][name] -= value
        self._lock.release()

    def get_info(self):
        return self.info
