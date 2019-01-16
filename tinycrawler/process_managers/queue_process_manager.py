"""Create a new manager of queue processes."""
from threading import Event
from ..utils import Logger
from typing import Dict
from ..processes.queue_process import QueueProcess


class QueueProcessManager:
    """Create a new manager of queue processes."""

    def __init__(self, stop: Event, logger: Logger, max_waiting_timeout: float, max_processes: int):
        """Create a new manager of queue processes.
            stop: Event, event to signal to process that the end has been reached.
            logger: Logger, logger where to log the process exceptions.
            max_waiting_timeout: float, maximum amount of time that the process has to wait doing nothing before quitting.
            max_processes: int, maximum number of processes of this kind that can be spawned.
        """
        self._stop = stop
        self._logger = logger
        self._max_waiting_timeout = max_waiting_timeout
        self._max_processes = max_processes
        self._processes = []

    @property
    def size(self):
        """Determine number of alive processes."""
        return [
            process.is_alive() for process in self._processes
        ]

    def join(self):
        """Join all processes."""
        for process in self._processes:
            process.join()

    def spawn(self)->QueueProcess:
        """Spawn a new process."""
        raise NotImplementedError(
            "Method `spawn` must be implemented by subclasses of QueueProcessManager")

    def can_spawn(self)->bool:
        """Return a boolean representing if a process can be spawned."""
        raise NotImplementedError(
            "Method `can_spawn` must be implemented by subclasses of QueueProcessManager")

    def update(self):
        """Cycles a check for spawn and eventually spawns new process."""
        if self.size < self._max_processes and self.can_spawn():
            new_process = self.spawn()
            new_process.start()
            self._processes.append(new_process)

    @property
    def _kwargs(self)->Dict:
        return {
            "stop": self._stop,
            "logger": self._logger,
            "max_waiting_timeout": self._max_waiting_timeout
        }
