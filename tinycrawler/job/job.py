"""Handle Job dispatching."""
from multiprocessing import Lock
from queue import Empty, Queue
from time import sleep, time
import traceback
from ..statistics import Speed, Time, Statistics
from ..log import Log


class Job(Queue):
    """Handle Job dispatching."""

    ATTEMPTS = 5

    def __init__(self, name: str, unit: str, logger: Log, statistics: Statistics):
        """Handle Job dispatching."""
        super().__init__()
        self._callback = None
        self._counter = 0
        self._name = name
        self._time = Time()
        self._logger = logger
        self._statistics = statistics
        self._growing_speed = Speed(unit)
        self._shrinking_speed = Speed(unit)
        self._lock = Lock()

    def set_callback(self, handler):
        """Set the jobs handler to dynamically grow processes number"""
        self._callback = handler

    def _update_put_statistics(self, value):
        self._statistics.add(
            self._name, "Queue {name}".format(name=self._name))
        self._growing_speed.update(1)
        self._statistics.set(self._name, "Growing speed",
                             self._growing_speed.get_formatted_speed())

    def _update_get_statistics(self, value):
        self._statistics.remove(
            self._name, "Queue {name}".format(name=self._name))
        self._shrinking_speed.update(1)
        self._statistics.set(self._name, "Shrinking speed",
                             self._shrinking_speed.get_formatted_speed())
        self._statistics.set("time", "Remaining {name} time".format(name=self._name),
                             self._time.get_remaining_time(self._growing_speed.get_speed(), self._shrinking_speed.get_speed(), self.len()))

    def put(self, value):
        """Add element to jobs, increase counter and update handler."""
        self._lock.acquire()
        self._counter += 1
        super()._put(value)
        self._lock.release()
        self._update_put_statistics(value)
        if self._callback and not self._callback.enough(self.len()):
            self._callback.add_process()

    def get(self):
        """Return new job and decrease counter."""
        for i in range(self.ATTEMPTS + 1):
            self._lock.acquire()
            if self._counter:
                break
            self._lock.release()
            if i == self.ATTEMPTS:
                raise Empty
            sleep(0.5)
        self._counter -= 1
        self._lock.release()
        value = super()._get()
        self._update_get_statistics(value)
        return value

    def len(self):
        return self._counter
