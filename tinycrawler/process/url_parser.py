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

    def __init__(self, path: str, jobs: FileJob, urls: UrlJob, robots: RobotsJob, use_beautiful_soup: bool, follow_robots_txt: bool):
        super().__init__(
            "{path}/graph".format(path=path), "urls parser", jobs)
        self._val = self._default_url_validator
        self._follow_robots_txt = follow_robots_txt
        self._urls = urls
        self._robots = robots
        if use_beautiful_soup:
            self._url_extractor = self._soup_url_extractor
            self._strainer = SoupStrainer('a', href=True)
        else:
            self._url_extractor = self._regex_url_extractor
            self._regex = re.compile(r"href=[\"\']?([^ >\"]+)[\"\']?")

    def _default_url_validator(self, url: str, logger: Log, statistics: Statistics):
        return True

    def _soup_url_extractor(self, response: Response):
        for anchor in BeautifulSoup(response.text, "lxml", parse_only=self._strainer).findAll(self._strainer):
            yield anchor.get("href")

    def _regex_url_extractor(self, response: Response):
        for partial_link in re.findall(self._regex, response.text):
            yield partial_link

    def _parser(self, response: Response, logger: Log, statistics: Statistics):
        url = response.url
        for partial_link in self._url_extractor(response):
            link = urljoin(url, partial_link)
            if not self._urls.contains(link) and valid(link) and self._val(link, logger, statistics) and (not self._follow_robots_txt or self._robots.can_fetch(link)):
                self._urls.put(link)

    def set_validator(self, url_validator: Callable[[str, Log, Statistics], bool]):
        """Set custom url validator.
            url_validator: Callable[[str, Log, Statistics], bool], the function used to validate urls.
        """
        self._val = url_validator
