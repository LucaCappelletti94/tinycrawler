from urllib.parse import urljoin
from bs4 import BeautifulSoup, SoupStrainer
from requests import Response
from typing import Callable

from validators import url as valid

from .parser import Parser
from ..log import Log
from ..statistics import Statistics
from ..job import UrlJob, FileJob, RobotsJob


class UrlParser(Parser):

    def __init__(self, path: str, jobs: FileJob, urls: UrlJob, robots: RobotsJob):
        super().__init__(
            "{path}/graph".format(path=path), "urls parser", jobs)
        self._val = self._default_url_validator
        self._urls = urls
        self._url_extractor = self._default_url_extractor
        self._robots = robots
        self._strainer = SoupStrainer('a', href=True)

    def _default_url_validator(self, url: str, logger: Log, statistics: Statistics):
        return True

    def _default_url_extractor(self, response: Response, urls: UrlJob, logger: Log, statistics: Statistics):
        url = response.url
        for partial_link in BeautifulSoup(response.text, "lxml", parse_only=self._strainer).findAll("a",  href=True):
            link = urljoin(url, partial_link["href"])
            if valid(link) and self._val(link, self._logger, self._statistics) and self._robots.can_fetch(link):
                urls.put(link)

    def _parser(self, response: Response, logger: Log, statistics: Statistics):
        self._url_extractor(response, self._urls, logger, statistics)

    def set_validator(self, url_validator: Callable[[str, Log, Statistics], bool]):
        """Set custom url validator.
            url_validator: Callable[[str, Log, Statistics], bool], the function used to validate urls.
        """
        self._val = url_validator

    def set_url_extractor(self, url_extractor: Callable[[Response, UrlJob, Log, Statistics], None]):
        """Set custom url extractor.
            url_extractor: Callable[[Response, UrlJob, Log, Statistics], None], the function used to extract urls.
        """
        self._url_extractor = url_extractor
