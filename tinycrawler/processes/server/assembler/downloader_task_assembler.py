"""Define a process that creates downloader tasks."""
from .task_assembler import TaskAssembler
from ....data import Urls, Proxies
from ....expirables import Url, Proxy, Domain, DownloaderTask
from ....exceptions import Sleep
from queue import Empty
from typing import Tuple


class DownloaderTaskAssembler(TaskAssembler):
    """Define a process that creates downloader tasks."""

    def __init__(self, urls: Urls, proxies: Proxies, **kwargs):
        """Define a process that creates downloader tasks."""
        super(DownloaderTaskAssembler, self).__init__(**kwargs)
        self._urls = urls
        self._proxies = proxies

    def _source(self)->Tuple[Url, Proxy]:
        try:
            url = self._urls.pop()
            return url, self._proxies.pop(url.domain)
        except Empty:
            raise Sleep

    def _job(self, url: Url, proxy: Proxy)->Tuple[DownloaderTask, Domain]:
        return DownloaderTask(
            proxy, url,  **self._task_kwargs
        ), proxy.ip if proxy.local else None
