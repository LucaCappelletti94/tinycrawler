"""Create a parser tasks worker process."""
from .worker import Worker
from ...expirables import ParserTask
from typing import Callable
import traceback
import sys
from bs4 import BeautifulSoup
from ...utils import url_to_path
from urllib.parse import urljoin
import validators


class Parser(Worker):
    """Create a parser tasks worker process."""

    def __init__(self, page: Callable = None, path: Callable = None, url: Callable = None, **kwargs):
        """Create a parser tasks worker process."""
        super(Parser, self).__init__(**kwargs)
        self._page = page if page is not None else lambda response, soup: response.text
        self._path = path if path is not None else url_to_path
        self._url = url if url is not None else lambda url: True

    def _work(self, parser_task: ParserTask)->bool:
        response = parser_task.response
        soup = BeautifulSoup(response.text, "html5lib")
        parser_task.urls = {url for url in self._urls(soup, response.url)}
        try:
            parser_task.page = self._page(response, soup)
            parser_task.path = self._path(response.url)
        except Exception:
            self._logger.error(traceback.print_exception(*sys.exc_info()))
            return False

        return True

    def _urls(self, soup: BeautifulSoup, root_url: str):
        for a in soup.find_all("a", href=True):
            url = urljoin(root_url, a.get("href"))
            if validators.url(url) and self._url(url):
                yield url
