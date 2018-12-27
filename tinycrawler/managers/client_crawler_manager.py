"""Create a client side object for managing the crawler data."""
from .crawler_manager import CrawlerManager
from ..expirables import ClientData
from typing import Dict
from ..utils import ClientQueueWrapper


class ClientCrawlerManager(CrawlerManager):
    """Create a client side object for managing the crawler data."""

    def __init__(self, host: str, port: int, authkey: str):
        """Create a client side object for managing the crawler data."""
        super(ClientCrawlerManager, self).__init__(
            host,
            port,
            authkey
        )
        for endpoint in self.endpoints:
            self.register(endpoint)

        self._urls = None
        self._end_event = None
        self._proxies = None
        self._clients = None
        self._responses = None
        self._downloader_tasks = None
        self._parser_tasks = None
        self._logger = None
        self._completed_downloader_tasks = None
        self._completed_parser_tasks = None

    @property
    def end_event(self):
        assert self._end_event is not None
        return self._end_event

    @property
    def urls(self):
        assert self._urls is not None
        return self._urls

    @property
    def proxies(self):
        assert self._proxies is not None
        return self._proxies

    @property
    def clients(self):
        assert self._clients is not None
        return self._clients

    @property
    def responses(self):
        assert self._responses is not None
        return self._responses

    @property
    def downloader_tasks(self):
        assert self._downloader_tasks is not None
        return self._downloader_tasks

    @property
    def parser_tasks(self):
        assert self._parser_tasks is not None
        return self._parser_tasks

    @property
    def logger(self):
        assert self._logger is not None
        return self._logger

    @property
    def completed_downloader_tasks(self):
        assert self._completed_downloader_tasks is not None
        return self._completed_downloader_tasks

    @property
    def completed_parser_tasks(self):
        assert self._completed_parser_tasks is not None
        return self._completed_parser_tasks

    def connect(self):
        """Handle connection to the server manager."""
        super(ClientCrawlerManager, self).connect()
        self._end_event = self.get_end_event()
        self._urls = ClientQueueWrapper(self.get_urls())
        self._proxies = ClientQueueWrapper(self.get_proxies())
        self._clients = self.get_clients()
        self._responses = ClientQueueWrapper(self.get_responses())
        self._downloader_tasks = ClientQueueWrapper(
            self.get_downloader_tasks())
        self._parser_tasks = ClientQueueWrapper(self.get_parser_tasks())
        self._logger = self.get_logger()
        self._completed_downloader_tasks = ClientQueueWrapper(
            self.get_completed_downloader_tasks())
        self._completed_parser_tasks = ClientQueueWrapper(
            self.get_completed_parser_tasks())

        self._client = ClientData(self.clients.get_new_client_id())
        self.register_client(self._client)

    def ___repr___(self)->Dict:
        """Return a dictionary representing the object."""
        return {
            **super(ClientCrawlerManager, self).___repr___(),
            "client": self._client.___repr___(),
            "urls": self.urls.___repr___(),
            "proxies": self.proxies.___repr___(),
            "responses": self.responses.___repr___(),
            "downloader_tasks": self.downloader_tasks.___repr___(),
            "parser_tasks": self.parser_tasks.___repr___(),
            "completed_downloader_tasks": self.completed_downloader_tasks.___repr___(),
            "completed_parser_tasks": self.completed_parser_tasks.___repr___(),
        }
