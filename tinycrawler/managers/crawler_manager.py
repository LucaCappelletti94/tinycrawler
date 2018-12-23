"""Abstract object for managing the crawler data."""
from multiprocessing import Queue
from multiprocessing.managers import BaseManager
from ..data import Robots, Urls, Proxies
from ..expirables import ExpirablesQueue, TasksQueue
from typing import List


class CrawlerManager(BaseManager):
    """Abstract object for managing the crawler data."""

    def __init__(self, host: str, port: int, authkey: str):
        """Abstract object for managing the crawler data."""
        super(CrawlerManager, self).__init__(
            address="{host}:{port}".format(
                host=host,
                port=port
            ),
            authkey=authkey
        )

    def get_robots(self)->Robots:
        """Return shared `Robots` object."""
        raise NotImplementedError(
            "Method `get_robots` has to be implemented by subclass."
        )

    def get_urls(self)->Urls:
        """Return shared `Urls` object."""
        raise NotImplementedError(
            "Method `get_urls` has to be implemented by subclass."
        )

    def get_responses(self)->ExpirablesQueue:
        """Return shared `ExpirablesQueue` of `Responses` object."""
        raise NotImplementedError(
            "Method `get_responses` has to be implemented by subclass."
        )

    def get_proxies(self)->Proxies:
        """Return shared `Proxies` object."""
        raise NotImplementedError(
            "Method `get_proxies` has to be implemented by subclass."
        )

    def get_downloader_tasks(self)->TasksQueue:
        """Return shared `TasksQueue` of `DownloaderTask` object."""
        raise NotImplementedError(
            "Method `get_downloader_tasks` has to be implemented by subclass."
        )

    def get_parser_tasks(self)->TasksQueue:
        """Return shared `TasksQueue` of `ParserTask` object."""
        raise NotImplementedError(
            "Method `get_downloader_tasks` has to be implemented by subclass."
        )

    def get_completed_downloader_tasks(self)->Queue:
        """Return shared `Queue` of `DownloaderTask` object."""
        raise NotImplementedError(
            "Method `get_completed_downloader_tasks` has to be implemented by subclass."
        )

    def get_completed_parser_tasks(self)->Queue:
        """Return shared `Queue` of `ParserTask` object."""
        raise NotImplementedError(
            "Method `get_completed_parser_tasks` has to be implemented by subclass."
        )

    def get_new_client_id(self)->int:
        """Return new client id."""
        raise NotImplementedError(
            "Method `get_client_id` has to be implemented by subclass."
        )

    @property
    def endpoints(self)->List[str]:
        """Return list of valid endpoints."""
        return [
            service for service in dir(CrawlerManager)
            if callable(getattr(CrawlerManager, service)) and service.startswith("get_")
        ]
