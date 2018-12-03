from typing import Callable
from time import time, sleep


class ETA(dict):
    def __init__(self, timeout: float, custom_timeout: Callable[[object], float]=None):
        """
            timeout: float, default value to wait for.
            custom_timeout: Callable[[object], float], function to call to get the timeout for given value.
        """
        self._timeout = timeout
        if custom_timeout is None:
            self._get_timeout = self.default_timeout
        else:
            self._get_timeout = custom_timeout

    def __getitem__(self, key):
        return super().__getitem__(self.__keytransform__(key))

    def __setitem__(self, key, value):
        super().__setitem__(self.__keytransform__(key), value)

    def __keytransform__(self, key):
        return key

    def default_timeout(self, value):
        return self._timeout

    def add(self, value=None):
        self[value] = time() + self._get_timeout(self.__keytransform__(value))

    def is_ripe(self, value=None):
        if value in self:
            return time() > self[value]
        else:
            return True

    def wait_for(self, value=None):
        delta = self[value] - time()
        if delta > 0:
            sleep(delta)

    def unripe(self):
        t = time()
        return [
            key for key, value in self.items() if t < value
        ]
