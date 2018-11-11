from urllib.parse import urljoin
from bs4 import BeautifulSoup, SoupStrainer
from requests import Response
from typing import Callable

from validators import url as valid
import re
from .parser import Parser
from ..log import Log
from ..statistics import Statistics
from ..job import UrlJob, FileJob, RobotsJob


class UrlParser(Parser):

    def __init__(self, path: str, jobs: FileJob, urls: UrlJob, robots: RobotsJob, use_beautiful_soup: bool=False):
        super().__init__(
            "{path}/graph".format(path=path), "urls parser", jobs)
        self._val = self._default_url_validator
        self._urls = urls
        if use_beautiful_soup:
            self._url_extractor = self._soup_url_extractor
        else:
            self._url_extractor = self._regex_url_extractor
        self._robots = robots
        self._regex = re.compile(r"href=[\"\']?([^ >]+)[\"\']?")
        self._strainer = SoupStrainer('a', href=True)

    def _default_url_validator(self, url: str, logger: Log, statistics: Statistics):
        return True

    def _soup_url_extractor(self, response: Response):
        for anchor in BeautifulSoup(response.text, "lxml", parse_only=self._strainer).findAll(self._strainer):
            yield anchor.get("href")

    def _regex_url_extractor(self, response: Response):
        for partial_link in re.findall(self._regex, response.text):
            yield partial_link

    def _url_parser(self, response: Response, urls: UrlJob, logger: Log, statistics: Statistics):
        url = response.url
        for partial_link in self._url_extractor(response):
            link = urljoin(url, partial_link)
            if valid(link) and self._val(link, self._logger, self._statistics) and self._robots.can_fetch(link):
                urls.put(link)

    def _parser(self, response: Response, logger: Log, statistics: Statistics):
        self._url_parser(response, self._urls, logger, statistics)

    def set_validator(self, url_validator: Callable[[str, Log, Statistics], bool]):
        """Set custom url validator.
            url_validator: Callable[[str, Log, Statistics], bool], the function used to validate urls.
        """
        self._val = url_validator
