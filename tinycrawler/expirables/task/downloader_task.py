from .task import Task
from ..web import Url, Proxy


class DownloaderTask(Task):

    def __init__(self, proxy: Proxy, url: Url, **kwargs):
        """Create an unique task.
            proxy:Proxy, proxy to be used.
            url:Url, url to download from.
        """
        super(DownloaderTask, self).__init__(**kwargs)
        self._proxy = proxy
        self._url = url
        self._binary = None
        self._text = None
        self._response_status = None

    def use(self, **kwargs):
        super(DownloaderTask, self).use(**kwargs)
        self._proxy.use(domain=self._url.domain, **kwargs)
        self._url.use(**kwargs)

    def used(self, success: bool, **kwargs):
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
        if self._binary is None:
            raise ValueError("Binary was not elaborated yet.")
        return self._binary

    @property
    def response_status(self)->int:
        if self._response_status is None:
            raise ValueError("Response status was not elaborated yet.")
        return self._response_status

    @property
    def text(self)->str:
        if self._text is None:
            raise ValueError("Text was not elaborated yet.")
        return self._text

    @response_status.setter
    def response_status(self, response_status)->int:
        if self._response_status is not None:
            raise ValueError(
                "Response status has already been elaborated.")
        self._response_status = response_status

    @text.setter
    def text(self, text)->int:
        if self._text is not None:
            raise ValueError("Text has already been elaborated.")
        self._text = text

    @binary.setter
    def binary(self, binary: bool):
        if self._binary is not None:
            raise ValueError("Binary has already been elaborated.")
        self._binary = binary

    def ___repr___(self):
        return {
            **super(DownloaderTask, self).___repr___(),
            **{
                "task_type": "downloader task"
            }}
