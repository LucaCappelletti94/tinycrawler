"""Define abstract class for downloader task handler."""


class DownloaderTaskHandler:
    """Define abstract class for downloader task handler."""

    def __init__(self, **kwargs):
        """Define abstract class for downloader task handler."""
        super(DownloaderTaskHandler, self).__init__(**kwargs)
        self._urls = kwargs["urls"]
        self._proxies = kwargs["proxies"]
