"""Create an unique downloader task."""
from .task import Task
from ..web import Url, Proxy
from typing import Dict, Tuple


class DownloaderTask(Task):
    """Create an unique downloader task."""

    def __init__(self, proxy: Proxy, url: Url, **kwargs):
        """Create an unique downloader task.
            proxy:Proxy, proxy to be used.
            url:Url, url to download from.
        """
        super(DownloaderTask, self).__init__(**kwargs)
        assert isinstance(proxy, Proxy)
        assert isinstance(url, Url)
        self._proxy = proxy
        self._url = url
        self._binary = None
        self._text = None
        self._response_status = None

    def is_available(self, **kwargs) -> bool:
        return super(DownloaderTask, self).is_available(**kwargs) and self._proxy.is_available(domain=self._url.domain, **kwargs) and self._url.is_available(**kwargs)

    def use(self, **kwargs):
        """Update use status in proxy and url."""
        super(DownloaderTask, self).use(**kwargs)
        self._proxy.use(domain=self._url.domain, **kwargs)
        self._url.use(**kwargs)

    def used(self, **kwargs):
        """Update used status in proxy and url.
            success:bool, result of task
        """
        success = kwargs["success"]
        assert isinstance(success, bool)
        super(DownloaderTask, self).used(**kwargs)
        self._proxy.used(success=success, domain=self._url.domain)
        self._url.used(**kwargs)

    @property
    def proxy(self)->Proxy:
        """Return proxy data object."""
        return self._proxy.data

    @property
    def url(self)->str:
        """Return url string."""
        return self._url.url

    @property
    def data(self)->Tuple[Url, Proxy]:
        """Return task original data."""
        return self._url, self._proxy

    @property
    def binary(self)->bool:
        """Return boolean representing if request was to a binary file."""
        assert self._binary is not None
        return self._binary

    @property
    def response_status(self)->int:
        """Return response status of request."""
        assert self._response_status is not None
        return self._response_status

    @property
    def text(self)->str:
        """Return textual response."""
        assert self._text is not None
        return self._text

    @response_status.setter
    def response_status(self, response_status: int):
        """Set response status of request."""
        assert isinstance(response_status, int)
        assert self._response_status is None
        self._response_status = response_status

    @text.setter
    def text(self, text)->int:
        """Set textual response of request."""
        assert isinstance(text, str)
        assert self._text is None
        self._text = text

    @binary.setter
    def binary(self, binary: bool):
        """Set whetever response was binary or not."""
        assert isinstance(binary, bool)
        assert self._binary is None
        self._binary = binary

    def ___repr___(self)->Dict:
        """Return a dictionary representation of object."""
        return {
            **super(DownloaderTask, self).___repr___(),
            **{
                "task_type": "downloader task",
                "url": self._url.___repr___(),
                "proxy": self._proxy.___repr___(),
                "binary": self.binary if self._binary else None,
                "text": self.text if self._text else None,
                "response_status": self.response_status if self._response_status else None
            }}
