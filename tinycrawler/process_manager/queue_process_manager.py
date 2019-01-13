"""Create a new manager of queue processes."""
from threading import Event
from ..utils import Logger
from typing import Dict


class QueueProcessManager:
    """Create a new manager of queue processes."""

    def __init__(self, stop: Event, logger: Logger, max_waiting_timeout: float):
        """Create a new manager of queue processes.
            stop: Event, event to signal to process that the end has been reached.
            logger: Logger, logger where to log the process exceptions.
            max_waiting_timeout: float, maximum amount of time that the process has to wait doing nothing before quitting.
        """
        self._stop = stop
        self._logger = logger
        self._max_waiting_timeout = max_waiting_timeout
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

    def spawn(self):
        """Spawn a new process."""
        raise NotImplementedError(
            "Method spawn must be implemented by subclasses of QueueProcessManager")

    @property
    def _kwargs(self)->Dict:
        return {
            "stop": self._stop,
            "logger": self._logger,
            "max_waiting_timeout": self._max_waiting_timeout
        }
