"""Create a ProcessHandler for a specific target and name."""
import math
import traceback
from multiprocessing import Process, Value, cpu_count
from queue import Empty


class ProcessHandler:
    """Create a ProcessHandler for a specific target and name."""

    def __init__(self, name, jobs):
        """Init a ProcessHandler for a specific target."""
        self._processes = []
        self._name = name
        self._jobs = jobs
        self.MAXIMUM_PROCESSES = math.ceil(cpu_count())

    def set_statistics(self, statistics):
        self._statistics = statistics

    def set_logger(self, logger):
        self._logger = logger

    def bind(self):
        self._jobs.set_callback(self)

    def add_process(self):
        """Start a new process to the target and objective given in init."""
        name = self._get_name()
        p = Process(target=self._job_starter, args=(name,), name=name)
        p.start()
        self._processes.append(p)

    def enough(self, c):
        n = self.alives()
        return n * 50 > c or n > self.MAXIMUM_PROCESSES

    def _get_name(self):
        """Return new process identifier name."""
        return "{name} n.{alive}".format(name=self._name, alive=self.alives())

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
                self._statistics.add(
                    "processes", "{name} working".format(name=self._name))
            except Empty:
                self._log_finish_queue(name)
                break
            except KeyboardInterrupt:
                break
            except Exception:
                self._log_process_exception(name)

            try:
                self._target(job)
            except KeyboardInterrupt:
                self._statistics.remove(
                    "processes", "{name} working".format(name=self._name))
                break
            except Exception:
                self._log_process_exception(name)
            finally:
                self._statistics.remove(
                    "processes", "{name} working".format(name=self._name))

    def _job_starter(self, name):
        """Generic process wrapper."""
        self._logger.log("Starting process {name}".format(name=name))
        self._statistics.add(
            "processes", "{name} alive".format(name=self._name))
        try:
            self._job_loop(name)
        except KeyboardInterrupt:
            self._statistics.remove(
                "processes", "{name} alive".format(name=self._name))
            return None
        except Exception:
            self._log_process_exception(name)
        finally:
            self._statistics.remove(
                "processes", "{name} alive".format(name=self._name))

    def _target(self, job):
        raise NotImplementedError(
            "Subclasses of ProcessHandler must implemented method _target.")

    def alives(self):
        return sum([int(p.is_alive()) for p in self._processes])

    def join(self):
        """Waits for the parser process to terminate"""
        [p.join() for p in self._processes]
