from .task_assembler import TaskAssembler
from ....data import Urls, Proxies
from ....expirables import Url, Proxy, Domain, DownloaderTask
from ....exceptions import Sleep
from queue import Empty
from typing import Tuple


class DownloaderTaskAssembler(TaskAssembler):
    def __init__(self, urls: Urls, proxies: Proxies, **kwargs):
        super(DownloaderTaskAssembler, self).__init__(**kwargs)
        self._urls = urls
        self._proxies = proxies

    def _source(self)->Tuple[Url, Proxy]:
        try:
            return self._urls.pop(), self._proxies.pop()
        except Empty:
            raise Sleep

    def _job(self, url: Url, proxy: Proxy)->Tuple[DownloaderTask, Domain]:
        return DownloaderTask(
            proxy, url
        ), proxy.ip if proxy.local else None
