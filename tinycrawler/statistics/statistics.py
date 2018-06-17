import time
from collections import defaultdict
from datetime import datetime, timedelta
from multiprocessing import Lock


class Statistics:
    def __init__(self):
        self._informations = {}
        self._lock = Lock()

    def add(self, category, name, value=1):
        """Add value to category/name and updates total."""
        self._lock.acquire()
        if category not in self._informations:
            self._informations[category] = defaultdict(int)

        self._informations[category][name] += value
        self._lock.release()

    def set(self, category, name, value=1):
        """Add value to category/name and updates total."""
        self._lock.acquire()
        if category not in self._informations:
            self._informations[category] = defaultdict(int)

        self._informations[category][name] = value
        self._lock.release()

    def remove(self, category, name, value=1):
        """Remove value to category/name."""
        self._lock.acquire()
        self._informations[category][name] -= value
        self._lock.release()

    def get(self, category, name):
        """Remove value to category/name."""
        return self._informations[category][name]

    def get_informations(self):
        return self._informations

    def is_everything_dead(self):
        if 'processes' not in self._informations:
            return False
        return not sum([v for v in self._informations['processes'].values()])
