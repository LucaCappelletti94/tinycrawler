"""Server side object for managing the crawler data."""
from .crawler_manager import CrawlerManager
from ..data import Robots, Urls, Proxies, Clients
from ..expirables import ExpirablesQueue, TasksQueue, DownloaderTask, ParserTask, Response, ClientData, Proxy
from ..utils import ProxyData, Logger


class ServerCrawlerManager(CrawlerManager):
    """Server side object for managing the crawler data."""

    def __init__(self, host: str, port: int, authkey: str, **kwargs):
        """Create a server side object for managing the crawler data."""
        super(ServerCrawlerManager, self).__init__(
            host,
            port,
            authkey
        )

        self._robots = Robots(**kwargs)
        self._urls = Urls(**kwargs)
        self._proxies = Proxies(**kwargs)
        self._clients = Clients()
        self._responses = ExpirablesQueue(Response, **kwargs)
        self._downloader_tasks = TasksQueue(DownloaderTask)
        self._parser_tasks = TasksQueue(ParserTask)
        self._logger = Logger(**kwargs)
        self._completed_downloader_tasks = ExpirablesQueue(
            DownloaderTask,
            **kwargs
        )
        self._completed_parser_tasks = ExpirablesQueue(
            ParserTask,
            **kwargs
        )

        self.register(
            "get_robots",
            callable=lambda: self._robots
        )
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
            callable=lambda: self._downloader_tasks
        )
        self.register(
            "get_parser_tasks",
            callable=lambda: self._parser_tasks
        )
        self.register(
            "get_completed_downloader_tasks",
            callable=lambda: self._completed_downloader_tasks
        )
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

    def handle_client_registration(self, client: ClientData):
        """Handle client registration, eventually creating adhoc proxy."""
        if self._clients.is_new_ip(client.ip):
            self._proxies.add(Proxy(ProxyData(ip=client.ip.domain)))
        if client not in self._clients:
            self._clients.register(client)