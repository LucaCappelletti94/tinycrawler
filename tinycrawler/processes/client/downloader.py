"""Create a downloader tasks worker process."""
from .worker import Worker
from ...expirables import DownloaderTask
from ...exceptions import MaxFileSize
import requests
from binaryornot.helpers import is_binary_string
from user_agent import generate_user_agent


class Downloader(Worker):
    """Create a downloader tasks worker process."""

    def __init__(self, max_content_len: int, user_agent: str, email: str, *args, **kwargs):
        """Create a downloader tasks worker process.
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
        super(Downloader, self).__init__(*args, **kwargs)
        self._max_content_len = max_content_len
        self._user_agent = user_agent
        self._email = email

    def _work(self, downloader_task: DownloaderTask)->bool:
        try:
            response = requests.get(
                downloader_task.url,
                proxies=downloader_task.proxy,
                headers=self._headers,
                stream=True
            )

            small = False

            try:
                head = next(response.iter_content(1000))
            except StopIteration:
                head = response.text
                small = True

            if is_binary_string(head):
                downloader_task.binary = True
            elif not small and not self._is_content_len_valid(response.headers):
                raise MaxFileSize()
            else:
                downloader_task.binary = False
                downloader_task.text = response.text if not small else head
                downloader_task.response_status = response.status_code
        except (
            requests.ConnectionError,
            MaxFileSize
        ) as e:
            print(e)
            return False

        return True

    @property
    def _headers(self):
        return {
            'User-Agent': generate_user_agent() if self._user_agent == "*" else self._user_agent,
            'From': self._email
        }

    def _has_content_len(self, headers)->bool:
        """Determine if given headers contains key `Content-Length`."""
        return "Content-Length" in headers

    def _is_content_len_valid(self, headers)->bool:
        """Determine if given headers contains valid `Content-Length`."""
        return not self._has_content_len(headers) or headers["Content-Length"] <= self._max_content_len
