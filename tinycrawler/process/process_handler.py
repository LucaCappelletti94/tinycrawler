"""Create a ProcessHandler for a specific target and name."""
import time
import traceback
from abc import ABC
from multiprocessing import Process, Value, cpu_count
from queue import Empty


class ProcessHandler:
    """Create a ProcessHandler for a specific target and name."""

    MAXIMUM_PROCESSES = cpu_count()

    def __init__(self, name, jobs, statistics, logger):
        """Init a ProcessHandler for a specific target."""
        self._processes = []
        self._statistics = statistics
        self._logger = logger
        self._name = name
        self._jobs = jobs

    def _bind_jobs(self):
        self._jobs.set_job_handler(self)

    def add_process(self):
        """Start a new process to the target and objective given in init."""
        name = self._get_name()
        p = Process(target=self._job_starter, args=(name,), name=name)
        p.start()
        self._processes.append(p)

    def enough(self, c):
        n = self.alives()
        return n * 10 > c or n == self.MAXIMUM_PROCESSES

    def _get_name(self):
        """Return new process identifier name."""
        n = self.alives()
        return "%s n.%s" % (self._name, n)

    def _log_finish_queue(self, name):
        """Log process has finished jobs."""
        self._logger.log("Process %s: has finished queue" % (name))

    def _log_process_exception(self, name):
        """Log process has raised exception."""
        self._logger.error("Process %s: %s" % (name, traceback.format_exc()))

    def _job_loop(self, name):
        """Handle queue iterations."""
        while(True):
            try:
                job = self._jobs.get()
            except Empty:
                self._log_finish_queue(name)
                break
            self._statistics.add("process", self._name + " working")
            self._target(job)
            self._statistics.remove("process", self._name + " working")

    def _job_starter(self, name):
        """Generic process wrapper."""
        self._logger.log("Starting process %s" % name)
        self._statistics.add("process", self._name + " alive")
        try:
            self._job_loop(name)
        except Exception:
            self._log_process_exception(name)
        self._statistics.remove("process", self._name + " alive")

    def _target(self, job):
        raise NotImplementedError("You should implement target")

    def alives(self):
        return sum([int(p.is_alive()) for p in self._processes])

    def join(self):
        """Waits for the parser process to terminate"""
        [p.join() for p in self._processes]
