"""Handle Job dispatching."""
from multiprocessing import Lock
from queue import Empty, Queue
from time import sleep


class Job(Queue):
    """Handle Job dispatching."""

    def __init__(self, name, statistics):
        """Handle Job dispatching."""
        super().__init__()
        self._job_handler = None
        self._counter = 0
        self._name = name
        self._statistics = statistics
        self._lock = Lock()

    def set_job_handler(self, handler):
        """Set the jobs handler to dynamically grow processes number"""
        self._job_handler = handler

    def _callback(self):
        """If it is defined, the callback is called."""
        jh = self._job_handler
        if jh is not None and not jh.enough(self.len()):
            jh.add_process()

    def put(self, value):
        """Add element to jobs, increase counter and update handler."""
        self._lock.acquire()
        self._counter += 1
        super()._put(value)
        self._lock.release()
        self._put_statistics()
        self._callback()

    def _put_update_add_statistics(self):
        self._statistics.add(self._name, "Queue %s" % self._name)

    def _put_statistics(self):
        self._put_update_add_statistics()
        self._statistics.add(self._name, "Total %s" % self._name)

    def get(self):
        """Return new job and decrease counter."""
        i = 0
        while True:
            self._lock.acquire()
            if not self._counter:
                self._lock.release()
                i += 1
                sleep(0.5)
            else:
                break
            if i > 4:
                raise Empty
        self._counter -= 1
        self._lock.release()
        job = super()._get()
        self._statistics.remove(self._name, "Queue %s" % self._name)
        return job

    def len(self):
        return self._counter
