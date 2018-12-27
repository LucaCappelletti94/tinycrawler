"""Define abstract class for downloader task handler."""
from ...data import Urls, Proxies


class DownloaderTaskHandler:
    """Define abstract class for downloader task handler."""

    def __init__(self, **kwargs):
        """Define abstract class for downloader task handler."""
        super(DownloaderTaskHandler, self).__init__(**kwargs)
        urls, proxies = kwargs["urls"], kwargs["proxies"]
        assert isinstance(urls, Urls)
        assert isinstance(proxies, Proxies)
        self._urls = urls
        self._proxies = proxies
