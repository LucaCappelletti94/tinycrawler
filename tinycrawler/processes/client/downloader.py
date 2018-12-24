from .worker import Worker
from ...expirables import DownloaderTask
from ...exceptions import MaxFileSize
import requests
from typing import Tuple
from binaryornot.helpers import is_binary_string
from user_agent import generate_user_agent


class Downloader(Worker):
    def __init__(self, max_content_len: int, user_agent: str, email: str, *args, **kwargs):
        super(Downloader, self).__init__(*args, **kwargs)
        self._max_content_len = max_content_len
        self._user_agent = user_agent
        self._email = email

    def _job(
        self,
        downloader_task: DownloaderTask
    )->Tuple[DownloaderTask]:
        success = False
        status = DownloaderTask.FAILURE
        try:
            response = requests.get(
                downloader_task.url,
                proxies=downloader_task.proxy,
                headers=self._headers,
                stream=True
            )

            if is_binary_string(next(response.iter_content(1000))):
                downloader_task.binary = True
            elif not self._is_content_len_valid(response.headers):
                raise MaxFileSize()
            else:
                downloader_task.binary = False
                downloader_task.text = response.text
                downloader_task.response_status = response.status_code
            success, status = True, DownloaderTask.SUCCESS
        except (
            requests.ConnectionError,
            MaxFileSize,
            StopIteration
        ):
            pass

        downloader_task.used(success=success)
        downloader_task.status = status
        return (downloader_task,)

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
