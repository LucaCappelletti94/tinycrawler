"""Define a process that creates downloader tasks."""
from .task_assembler import TaskAssembler
from ....expirables import Url, Proxy, Domain, DownloaderTask
from ..downloader_task_handler import DownloaderTaskHandler
from typing import Tuple


class DownloaderTaskAssembler(DownloaderTaskHandler, TaskAssembler):
    """Define a process that creates downloader tasks."""

    def _source(self)->Tuple[Url, Proxy]:
        url = self._urls.pop()
        return url, self._proxies.pop(url.domain)

    def _job(self, *args)->Tuple[DownloaderTask, Domain]:
        url, proxy = args
        assert isinstance(url, Url)
        assert isinstance(proxy, Proxy)
        return DownloaderTask(
            proxy, url,  **self._task_kwargs
        ), proxy.ip if proxy.local else None
