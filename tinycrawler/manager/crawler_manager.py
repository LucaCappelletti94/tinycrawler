"""Abstract object for managing the crawler data."""
from multiprocessing import Queue
from multiprocessing.managers import BaseManager
from ..data import Robots, Urls, Proxies
from ..expirables import ExpirablesQueue, TasksQueue


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
        raise NotImplementedError(
            "Method `get_robots` has to be implemented by subclass."
        )

    def get_urls(self)->Urls:
        raise NotImplementedError(
            "Method `get_urls` has to be implemented by subclass."
        )

    def get_responses(self)->ExpirablesQueue:
        raise NotImplementedError(
            "Method `get_responses` has to be implemented by subclass."
        )

    def get_proxies(self)->Proxies:
        raise NotImplementedError(
            "Method `get_proxies` has to be implemented by subclass."
        )

    def get_downloader_tasks(self)->TasksQueue:
        raise NotImplementedError(
            "Method `get_downloader_tasks` has to be implemented by subclass."
        )

    def get_parser_tasks(self)->TasksQueue:
        raise NotImplementedError(
            "Method `get_downloader_tasks` has to be implemented by subclass."
        )

    def get_completed_downloader_tasks(self)->Queue:
        raise NotImplementedError(
            "Method `get_completed_downloader_tasks` has to be implemented by subclass."
        )

    def get_completed_parser_tasks(self)->Queue:
        raise NotImplementedError(
            "Method `get_completed_parser_tasks` has to be implemented by subclass."
        )

    def get_client_id(self)->int:
        raise NotImplementedError(
            "Method `get_client_id` has to be implemented by subclass."
        )
