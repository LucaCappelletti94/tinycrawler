from urllib.parse import urljoin
from .process_handler import ProcessHandler
from ..log import Log
from bs4 import BeautifulSoup
from ..statistics import Statistics
from ..robots import Robots
from ..urls import Urls
from requests import Response
import validators
from typing import Callable
from multiprocessing import Event, Value
from queue import Empty, Queue


class Parser(ProcessHandler):
    def __init__(self, process_spawn_event: Event, process_callback_event: Event, pages_number: Value, urls_number: Value, responses: Queue, urls: Urls, robots: Robots, file_parser: Callable[[str, BeautifulSoup, Log], None], url_validator: Callable[[str, Log], bool], statistics: Statistics, logger: Log, follow_robots_txt: bool, parser_library: str):
        super().__init__("Parser", statistics, process_spawn_event)
        self._urls, self._responses, self._process_callback_event, self._pages_number, self._urls_number, self._robots, self._follow_robots_txt, self._file_parser,  self._url_validator, self._logger, self._parser_library = urls, responses, process_callback_event, pages_number, urls_number, robots, follow_robots_txt, file_parser, url_validator, logger, parser_library

    def _url_parser(self, page_url: str, soup: BeautifulSoup):
        urls = set()
        for a in soup.findAll("a", href=True):
            url = urljoin(page_url, a.get("href"))
            if validators.url(url) and self._url_validator(url, self._logger) and (not self._follow_robots_txt or self._robots.can_fetch(url)):
                urls.add(url)
        if urls:
            n = self._urls.put(urls)
            if n > 0:
                self._urls_number.value += n
                self._process_callback_event.set()

    def _enough(self, active_processes):
        return active_processes*20 > self._pages_number.value

    def _target(self, response: Response):
        """Parse the downloaded files, cleans them and extracts urls"""
        soup = BeautifulSoup(response.text, self._parser_library)
        self._url_parser(response.url, soup)
        self._file_parser(response.url, soup, self._logger)

    def _get_job(self):
        response = self._responses.get_nowait()
        self._pages_number.value -= 1
        return (response,)
