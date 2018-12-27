"""Abstract object for managing the crawler data."""
from multiprocessing import Queue
from multiprocessing.managers import BaseManager
from ..data import Urls, Proxies, Clients
from ..expirables import ExpirablesQueue, TasksQueue, ClientData
from ..utils import Printable
from typing import List, Dict
from threading import Event


class CrawlerManager(BaseManager, Printable):
    """Abstract object for managing the crawler data."""

    def __init__(self, host: str, port: int, authkey: str):
        """Abstract object for managing the crawler data."""
        assert isinstance(host, str)
        assert isinstance(port, int)
        assert isinstance(authkey, bytes)
        super(CrawlerManager, self).__init__(
            address=(host, port),
            authkey=authkey
        )

    def get_urls(self)->Urls:
        """Return shared `Urls` object."""
        raise NotImplementedError(
            "Method `get_urls` has to be registered by subclass and not directly called."
        )

    def get_end_event(self)->Event:
        """Return shared end event Event."""
        raise NotImplementedError(
            "Method `get_end_event` has to be registered by subclass and not directly called."
        )

    def get_responses(self)->ExpirablesQueue:
        """Return shared `ExpirablesQueue` of `Responses` object."""
        raise NotImplementedError(
            "Method `get_responses` has to be registered by subclass and not directly called."
        )

    def get_proxies(self)->Proxies:
        """Return shared `Proxies` object."""
        raise NotImplementedError(
            "Method `get_proxies` has to be registered by subclass and not directly called."
        )

    def get_downloader_tasks(self)->TasksQueue:
        """Return shared `TasksQueue` of `DownloaderTask` object."""
        raise NotImplementedError(
            "Method `get_downloader_tasks` has to be registered by subclass and not directly called."
        )

    def get_parser_tasks(self)->TasksQueue:
        """Return shared `TasksQueue` of `ParserTask` object."""
        raise NotImplementedError(
            "Method `get_downloader_tasks` has to be registered by subclass and not directly called."
        )

    def get_completed_downloader_tasks(self)->Queue:
        """Return shared `Queue` of `DownloaderTask` object."""
        raise NotImplementedError(
            "Method `get_completed_downloader_tasks` has to be registered by subclass and not directly called."
        )

    def get_completed_parser_tasks(self)->Queue:
        """Return shared `Queue` of `ParserTask` object."""
        raise NotImplementedError(
            "Method `get_completed_parser_tasks` has to be registered by subclass and not directly called."
        )

    def get_clients(self)->Clients:
        """Return shared `Clients` object."""
        raise NotImplementedError(
            "Method `get_clients` has to be registered by subclass and not directly called."
        )

    def get_logger(self)->Clients:
        """Return shared `Logger` object."""
        raise NotImplementedError(
            "Method `get_logger` has to be registered by subclass and not directly called."
        )

    def register_client(self, client: ClientData):
        """Register client on server.
            client: ClientData, client to be registered
        """
        raise NotImplementedError(
            "Method `register_client` has to be registered by subclass and not directly called."
        )

    @property
    def endpoints(self)->List[str]:
        """Return list of valid endpoints."""
        return [
            service for service in set(dir(CrawlerManager)) - set(dir(BaseManager))
            if callable(getattr(CrawlerManager, service)) and (service.startswith("get_") or service == "register_client")
        ]

    def ___repr___(self)->Dict:
        """Return a dictionary representing the object."""
        return {
            "address": self.address[0]
        }
