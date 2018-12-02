"""Create a ProcessHandler for a specific target and name."""
import math
import traceback
from multiprocessing import Process, cpu_count, Event
from queue import Empty
from ..statistics import Statistics


class ProcessHandler:
    """Create a ProcessHandler for a specific target and name."""

    def __init__(self, name: str, statistics: Statistics, process_spawn_event: Event):
        """Init a ProcessHandler for a specific target."""
        self._processes = []
        self._name = name
        self._statistics = statistics
        self._process_spawn_event = process_spawn_event
        self.MAXIMUM_PROCESSES = cpu_count()

    def job_event_check(self):
        n = self.alive_processes_number()
        if self._process_spawn_event.is_set():
            self._process_spawn_event.clear()
            if n < self.MAXIMUM_PROCESSES and not self._enough(n):
                self.add_process()
        self._statistics.set(
            "Processes", "Total {name}".format(name=self._name), n)

    def add_process(self):
        """Start a new process to the target and objective given in init."""
        name = self._get_name()
        p = Process(target=self._job_starter, args=(name,), name=name)
        p.start()
        self._processes.append(p)

    def _get_name(self):
        """Return new process identifier name."""
        return "{name} n.{alive}".format(name=self._name, alive=self.alive_processes_number())

    def _job_loop(self, name):
        """Handle queue iterations."""
        while(True):
            try:
                self._target(*self._get_job())
            except Empty:
                break

    def _job_starter(self, name):
        """Generic process wrapper."""
        self._job_loop(name)

    def _enough(self, active_processes: int)->bool:
        raise NotImplementedError(
            "Subclasses of ProcessHandler must implement method _enough.")

    def _target(self, job):
        raise NotImplementedError(
            "Subclasses of ProcessHandler must implement method _target.")

    def _get_job(self):
        raise NotImplementedError(
            "Subclasses of ProcessHandler must implement method _get_job.")

    def alive_processes_number(self):
        return sum([p.is_alive() for p in self._processes])

    def join(self):
        """Waits for the parser process to terminate"""
        [p.join() for p in self._processes]
