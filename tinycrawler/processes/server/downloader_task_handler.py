"""Define abstract class for downloader task handler."""
from ...data import Urls, Proxies


class DownloaderTaskHandler:
    """Define abstract class for downloader task handler."""

    def __init__(self, urls: Urls, proxies: Proxies, **kwargs):
        """Define abstract class for downloader task handler.
            urls: Urls, queue of urls to use to build tasks.
            proxies: Proxies, queue of proxies to use to build tasks.
        """
        super(DownloaderTaskHandler, self).__init__(**kwargs)
        self._urls = urls
        self._proxies = proxies
