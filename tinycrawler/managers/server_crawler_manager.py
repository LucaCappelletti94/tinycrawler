"""Server side object for managing the crawler data."""
from .crawler_manager import CrawlerManager
from ..data import Urls, Proxies, Clients
from ..expirables import ExpirablesQueue, TasksQueue, TasksSink, ClientData, Proxy
from ..utils import ProxyData, Logger, ServerQueueWrapper
from typing import Dict
from multiprocessing import Event


class ServerCrawlerManager(CrawlerManager):
    """Server side object for managing the crawler data."""

    def __init__(self, host: str, port: int, authkey: str, **kwargs):
        """Create a server side object for managing the crawler data."""
        super(ServerCrawlerManager, self).__init__(
            host,
            port,
            authkey
        )
        self._urls = ServerQueueWrapper(Urls(**kwargs))
        self._proxies = ServerQueueWrapper(Proxies(**kwargs))
        self._clients = Clients()
        self._end_event = Event()
        self._responses = ServerQueueWrapper(
            ExpirablesQueue()
        )
        self._downloader_tasks = TasksQueue()
        self._parser_tasks = TasksQueue()
        self._wrapped_downloader_tasks = ServerQueueWrapper(
            self._downloader_tasks)
        self._wrapped_parser_tasks = ServerQueueWrapper(self._parser_tasks)
        self._logger = Logger(**kwargs)
        self._completed_downloader_tasks = ServerQueueWrapper(
            TasksSink(self._downloader_tasks))
        self._completed_parser_tasks = ServerQueueWrapper(
            TasksSink(self._parser_tasks))

        self.register(
            "get_urls",
            callable=lambda: self._urls
        )
        self.register(
            "get_proxies",
            callable=lambda: self._proxies
        )
        self.register(
            "get_responses",
            callable=lambda: self._responses
        )
        self.register(
            "get_downloader_tasks",
            callable=lambda: self._wrapped_downloader_tasks
        )
        self.register(
            "get_parser_tasks",
            callable=lambda: self._wrapped_parser_tasks
        )
        self.register(
            "get_completed_downloader_tasks",
            callable=lambda: self._completed_downloader_tasks
        )R£TLYç°
        self.register(
            "get_completed_parser_tasks",
            callable=lambda: self._completed_parser_tasks
        )
        self.register(
            "get_clients",
            callable=lambda: self._clients
        )
        self.register(
            "get_logger",
            callable=lambda: self._logger
        )
        self.register(
            "register_client",
            callable=self.handle_client_registration
        )
        self.register(
            "get_end_event",
            callable=lambda: self._end_event
        )

    def handle_client_registration(self, client: ClientData):
        """Handle client registration, eventually creating adhoc proxy.
            client: ClientData, the client to be registered
        """
        assert isinstance(client, ClientData)
        if self._clients.is_new_ip(client.ip):
            self._proxies.add(Proxy(ProxyData(ip=client.ip.domain)))
        if client not in self._clients:
            self._clients.register(client)

    def ___repr___(self)->Dict:
        """Return a dictionary representing the object."""
        return {
            **super(ServerCrawlerManager, self).___repr___(),
            "urls": self._urls.___repr___(),
            "proxies": self._proxies.___repr___(),
            "clients": self._clients.___repr___(),
            "responses": self._responses.___repr___(),
            "downloader_tasks": self._downloader_tasks.___repr___(),
            "parser_tasks": self._parser_tasks.___repr___(),
            "completed_downloader_tasks": self._completed_downloader_tasks.___repr___(),
            "completed_parser_tasks": self._completed_parser_tasks.___repr___(),
        }
