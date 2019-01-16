"""Create a manager of parser tasks worker processes."""
from .worker_manager import WorkerManager
from ...processes import Parser
from typing import Callable


class ParserManager(WorkerManager):
    """Create a manager of parser tasks worker processes."""

    def __init__(self, page: Callable, path: Callable, url: Callable, **kwargs):
        """Create a manager of parser tasks worker processes.
            stop: Event, event to signal to process that the end has been reached.
            logger: Logger, logger where to log the process exceptions.
            max_waiting_timeout: float, maximum amount of time that the process has to wait doing nothing before quitting.
            max_processes: int, maximum number of processes of this kind that can be spawned.
            client_data: ClientData, informations about the client that is running this Worker process.
            tasks: TasksQueue, queue of tasks that the worker will run through.
            completed_tasks: TasksSink, queue of tasks where the worker will put completed tasks.
            page: Callable, function that handles the parsing of the page.
            path: Callable, function that handles the generation of the path where to save the page.
            url: Callable, function that handles the validation of an url.
        """
        super(ParserManager, self).__init__(**kwargs)
        self._page = page
        self._path = path
        self._url = url

    def spawn(self)->Parser:
        """Spawn a new Parser process."""
        return Parser(
            **super(ParserManager, self)._kwargs,
            page=self._page,
            path=self._path,
            url=self._url
        )
