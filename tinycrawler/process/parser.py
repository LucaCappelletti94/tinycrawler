from urllib.parse import urljoin
from .process_handler import ProcessHandler
from ..log import Log
from bs4 import BeautifulSoup
from ..statistics import Statistics
from ..job import UrlJob, FileJob, RobotsJob
from requests import Response
import validators
from typing import Callable


class Parser(ProcessHandler):
    def __init__(self, jobs: FileJob, urls: UrlJob, robots: RobotsJob, file_parser: Callable[[str, BeautifulSoup, Log], None], url_validator: Callable[[str, Log], bool], statistics: Statistics, logger: Log, follow_robots_txt: bool):
        super().__init__("Parser", jobs, statistics)
        self._urls, self._robots, self._follow_robots_txt, self._file_parser,  self._url_validator, self._logger = urls, robots, follow_robots_txt, file_parser, url_validator, logger

    def _url_parser(self, page_url: str, soup: BeautifulSoup):
        urls = []
        for a in soup.findAll("a", href=True):
            url = urljoin(page_url, a.get("href"))
            if validators.url(url) and self._url_validator(url, self._logger) and (not self._follow_robots_txt or self._robots.can_fetch(url)):
                urls.append(url)
        if urls:
            self._urls.put(urls)

    def _target(self, response: Response):
        """Parse the downloaded files, cleans them and extracts urls"""
        soup = BeautifulSoup(response.text, "html5lib")
        self._url_parser(response.url, soup)
        self._file_parser(response.url, soup, self._logger)
