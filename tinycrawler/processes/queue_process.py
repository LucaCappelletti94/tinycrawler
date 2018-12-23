"""Create a process object specialized for consumer-producer queues."""
from multiprocessing import Process
from threading import Event
from typing import Tuple
from queue import Empty
from ..utils import Logger
import traceback
import sys


class QueueProcess(Process):
    """Create a process object specialized for consumer-producer queues."""

    def __init__(self, stop: Event, logger: Logger):
        """Create a process object specialized for consumer-producer queues."""
        super(QueueProcess, self).__init__(
            target=self._loop
        )
        self._stop = stop
        self._logger = logger

    def _loop(self):
        """Execute all the available jobs."""
        while not self._stop.is_set():
            try:
                self._sink(
                    *self._job(
                        *self._source()
                    )
                )
            except Empty:
                break
            except Exception:
                self._logger.error(traceback.print_exception(*sys.exc_info()))
                break

    def _sink(self, *args):
        """Handle the elaboration of the results from job."""
        raise NotImplementedError(
            "Method `_sink` has to implement by subclasses of QueueProcess"
        )

    def _source(self, *args)->Tuple:
        """Handle the production of the raw input from job."""
        raise NotImplementedError(
            "Method `_source` has to implement by subclasses of QueueProcess"
        )

    def _job(self, *args)->Tuple:
        """Handle the execution of the job."""
        raise NotImplementedError(
            "Method `_job` has to implement by subclasses of QueueProcess"
        )
