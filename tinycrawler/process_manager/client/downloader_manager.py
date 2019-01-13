"""Create a manager of downloader tasks worker processes."""
from .worker_manager import WorkerManager
from ...processes import Downloader


class DownloaderManager(WorkerManager):
    """Create a manager of downloader tasks worker processes."""

    def __init__(self, max_content_len: int, user_agent: str, email: str, **kwargs):
        """Create a manager of downloader tasks worker processes.
            stop: Event, event to signal to process that the end has been reached.
            logger: Logger, logger where to log the process exceptions.
            max_waiting_timeout: float, maximum amount of time that the process has to wait doing nothing before quitting.
            client_data: ClientData, informations about the client that is running this Worker process.
            tasks: TasksQueue, queue of tasks that the worker will run through.
            completed_tasks: TasksSink, queue of tasks where the worker will put completed tasks.
            max_content_len: int, maximum content size of downloaded pages.
            user_agent: str, user agent to use for requests. Use `*` for random useragent.
            email: str, email to offer for contact pourposes from website admins.
        """
        super(DownloaderManager, self).__init__(**kwargs)
        self._max_content_len = max_content_len
        self._user_agent = user_agent
        self._email = email

    def spawn(self)->Downloader:
        """Spawn a new Downloader process."""
        return Downloader(
            **super(DownloaderManager, self)._kwargs,
            max_content_len=self._max_content_len,
            user_agent=self._user_agent,
            email=self._email
        )
