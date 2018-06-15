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
        if self._job_handler is not None:
            if not self._job_handler.are_processes_enough(self._counter):
                self._job_handler.add_process()

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
        self._lock.acquire()
        if self._counter == 0:
            self._lock.release()
            raise Empty
        else:
            self._counter -= 1
            job = super()._get()
        self._lock.release()
        self._statistics.remove(self._name, "Queue %s" % self._name)
        return job

    def get_counter(self):
        return self._counter
