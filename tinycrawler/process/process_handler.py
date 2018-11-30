"""Create a ProcessHandler for a specific target and name."""
import math
import traceback
from multiprocessing import Process, Value, cpu_count
from queue import Empty
from ..statistics import Statistics
from ..job import Job


class ProcessHandler:
    """Create a ProcessHandler for a specific target and name."""

    def __init__(self, name: str, jobs: Job, statistics: Statistics):
        """Init a ProcessHandler for a specific target."""
        self._processes = []
        self._name = name
        self._jobs = jobs
        self._statistics = statistics
        self.MAXIMUM_PROCESSES = cpu_count()

    def bind(self):
        self._jobs.set_callback(self)

    def add_process(self):
        """Start a new process to the target and objective given in init."""
        name = self._get_name()
        p = Process(target=self._job_starter, args=(name,), name=name)
        p.start()
        self._processes.append(p)

    def enough(self, c):
        n = self.alive_processes_number()
        return n * 50 > c or n >= self.MAXIMUM_PROCESSES

    def _get_name(self):
        """Return new process identifier name."""
        return "{name} n.{alive}".format(name=self._name, alive=self.alive_processes_number())

    def _remove_worker(self):
        self._statistics.remove(
            "processes", "{name} working".format(name=self._name))

    def _job_loop(self, name):
        """Handle queue iterations."""
        while(True):
            try:
                job = self._jobs.get()
                self._statistics.add(
                    "processes", "{name} working".format(name=self._name))
            except (Empty, KeyboardInterrupt):
                break

            try:
                self._target(job)
                self._remove_worker()
            except KeyboardInterrupt:
                self._remove_worker()
                break

    def _job_starter(self, name):
        """Generic process wrapper."""
        self._statistics.add(
            "processes", "{name} alive".format(name=self._name))
        try:
            self._job_loop(name)
        except KeyboardInterrupt:
            pass
        finally:
            self._statistics.remove(
                "processes", "{name} alive".format(name=self._name))

    def _target(self, job):
        raise NotImplementedError(
            "Subclasses of ProcessHandler must implement method _target.")

    def alive_processes_number(self):
        return sum([int(p.is_alive()) for p in self._processes])

    def join(self):
        """Waits for the parser process to terminate"""
        [p.join() for p in self._processes]
