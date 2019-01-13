"""Create a process object specialized for consumer-producer queues."""
from multiprocessing import Process
from threading import Event
from typing import Tuple
from queue import Empty
from ..utils import Logger
import traceback
import time
import sys


class QueueProcess(Process):
    """Create a process object specialized for consumer-producer queues."""

    def __init__(self, stop: Event, logger: Logger, max_waiting_timeout: float, **kwargs):
        """Create a process object specialized for consumer-producer queues.
            stop: Event, event to signal to process that the end has been reached.
            logger: Logger, logger where to log the process exceptions.
            max_waiting_timeout: float, maximum amount of time that the process has to wait doing nothing before quitting.
        """
        super(QueueProcess, self).__init__(
            target=self._loop
        )
        assert isinstance(max_waiting_timeout, (int, float))
        self._stop = stop
        self._logger = logger
        self._max_waiting_timeout = max_waiting_timeout

    def _loop(self):
        """Execute all the available jobs."""
        self._last_sleep_time = time.time()
        while not self._stop.is_set() and time.time() - self._last_sleep_time < self._max_waiting_timeout:
            try:
                self._sink(
                    *self._job(
                        *self._source()
                    )
                )
                self._last_sleep_time = time.time()
            except Empty:
                time.sleep(1)
            except Exception:
                self._logger.error(traceback.print_exception(*sys.exc_info()))
                break

    def _sink(self, *args):
        """Handle the elaboration of the results from job."""
        raise NotImplementedError(
            "Method `_sink` has to implement by subclasses of QueueProcess"
        )

    def _source(self)->Tuple:
        """Handle the production of the raw input from job."""
        raise NotImplementedError(
            "Method `_source` has to implement by subclasses of QueueProcess"
        )

    def _job(self, *args)->Tuple:
        """Handle the execution of the job."""
        raise NotImplementedError(
            "Method `_job` has to implement by subclasses of QueueProcess"
        )
