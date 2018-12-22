from .task import Task
from ..web import Url, Proxy, Response


class DownloaderTask(Task):

    def __init__(self, proxy: Proxy, url: Url, task_id: int, **kwargs):
        """Create an unique task.
            task_id:int, unique identifier of current task.
            proxy:Proxy, proxy to be used.
            url:Url, url to download from.
        """
        super(DownloaderTask, self).__init__(task_id, **kwargs)
        self._proxy = proxy
        self._url = url
        self._binary = False
        self._response = None

    def use(self, **kwargs):
        super(DownloaderTask, self).use(**kwargs)
        self._proxy.use(domain=self._url.domain, **kwargs)
        self._url.use(**kwargs)

    def used(self, success: bool):
        super(DownloaderTask, self).used()
        self._proxy.used(success=success, domain=self._url.domain)

    @property
    def proxy(self)->Proxy:
        return self._proxy.data

    @property
    def url(self)->str:
        return self._url.url

    @property
    def binary(self)->bool:
        return self._binary

    @property
    def response(self)->str:
        if self._response is None:
            raise ValueError("Response was not elaborated yet.")
        return self._response

    @response.setter
    def response(self, response: str):
        if self._response is not None:
            raise ValueError("Response has already been elaborated.")
        self._response = Response(response)

    @binary.setter
    def binary(self, binary: bool):
        self._binary = binary

    def ___repr___(self):
        return {
            **super(DownloaderTask, self).___repr___(),
            **{
                "task_type": "downloader task"
            }}
