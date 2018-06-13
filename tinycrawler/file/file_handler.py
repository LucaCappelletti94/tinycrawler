import re
import time
from multiprocessing import Queue
from urllib.parse import urljoin, urlparse

import validators

from .file_parser import file_parser


class file_handler:

    def __init__(self, files, urls, path, statistics, logger, timeout=30):

        self._urls = urls
        self._url_regex = re.compile(r"href=[\"']([^\"#\']+)[\"']")
        self._statistics = statistics
        self._url_validator = lambda url: True
        self._custom_file_parser = lambda request_url, text, logger: text

        self._file_parsers = []
        self._url_parsers = []
        self._custom_url_extractor = None

        for i in range(2):
            self._file_parsers.append(file_parser(
                input_queue=files[0],
                statistics=statistics,
                logger=logger,
                path="%s/%s" % (path, "webpages"),
                timeout=timeout
            ))

        for i in range(2):
            self._url_parsers.append(file_parser(
                input_queue=files[1],
                statistics=statistics,
                logger=logger,
                path="%s/%s" % (path, "graph"),
                timeout=timeout
            ))

    def run(self):
        """Starts the parser"""
        while not self._statistics.has_bitten():
            time.sleep(1)

        for file_parser in self._file_parsers:
            file_parser.set_custom_parser(self._default_file_parser)
            file_parser.run("file")

        for url_parser in self._url_parsers:
            url_parser.set_custom_parser(self._extract_valid_urls)
            url_parser.run("url")

    def join(self):
        for file_parser in self._file_parsers:
            file_parser.join()
        for url_parser in self._url_parsers:
            url_parser.join()

    def _url_extractor(self, request_url, text, logger):
        urls = []
        for link in re.findall(self._url_regex, text):
            url = urljoin(request_url, link)
            if validators.url(url):
                if self._url_validator(url) and not self._urls.contains(url):
                    urls.append(url)
        return urls

    def _extract_valid_urls(self, request_url, text, logger):
        urls = self._url_extractor(request_url, text, logger)
        [self._urls.put(url) for url in urls]
        self._statistics.add_parsed_graph()
        self._statistics.add_total(len(urls))
        return urls

    def _default_file_parser(self, request_url, text, logger):
        text = self._custom_file_parser(request_url, text, logger)
        if not text:
            self._statistics.add_discarted()
            self._statistics.add_parsed(0)
        else:
            self._statistics.add_parsed(len(text))
        return text

    def set_url_validator(self, url_validator):
        self._url_validator = url_validator

    def set_url_extractor(self, url_extractor):
        self._url_extractor = url_extractor

    def set_file_parser(self, parser):
        self._custom_file_parser = parser
