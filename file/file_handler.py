from multiprocessing import Queue
import time
from urllib.parse import urljoin, urlparse
import validators

from .file_parser import file_parser
from .file_writer import file_writer

import re

class file_handler:

    def __init__(self, files, urls, path, statistics, logger, timeout = 30):

        parsed = Queue()
        graph = Queue()
        self._urls = urls
        self._url_regex = re.compile(r"href=\"([^\"#]+)\"")
        self._statistics = statistics
        self._custom_url_validator = lambda url: True
        self._custom_file_parser = lambda request_url, text, logger: text

        self._file_parsers = []

        for i in range(2):
            self._file_parsers.append(file_parser(
                input_queue = files[0],
                output_queue = parsed,
                statistics = statistics,
                logger = logger,
                timeout = timeout
            ))

        self._url_parser = file_parser(
            input_queue = files[1],
            output_queue = graph,
            statistics = statistics,
            logger = logger,
            timeout = timeout
        )
        self._webpages_writer = file_writer(parsed, "%s/%s"%(path, "webpages"), statistics, logger, timeout)
        self._graph_writer = file_writer(graph, "%s/%s"%(path, "graph"), statistics, logger, timeout)

    def run(self):
        """Starts the parser"""
        while not self._statistics.has_bitten():
            time.sleep(1)

        self._url_parser.set_custom_parser(self._extract_valid_urls)
        self._webpages_writer.set_write_callback(self._write_counter)

        for file_parser in self._file_parsers:
            file_parser.set_custom_parser(self._default_file_parser)
            file_parser.run("file")

        self._url_parser.run("url")
        self._webpages_writer.run()
        self._graph_writer.run()

    def join(self):
        for file_parser in self._file_parsers:
            file_parser.join()
        self._url_parser.join()
        self._webpages_writer.join()
        self._graph_writer.join()

    def _extract_valid_urls(self, request_url, text, logger):
        urls = []
        total = 0
        for link in re.findall(self._url_regex, text):
            url = urljoin(request_url, link)
            if validators.url(url):
                urls.append(url)
                if self._custom_url_validator(url) and not self._urls.contains(url):
                    total += 1
                    self._urls.put(url)
        self._statistics.add_parsed_graph()
        self._statistics.add_total(total)
        return urls

    def _write_counter(self):
        self._statistics.add_written()

    def _default_file_parser(self, request_url, text, logger):
        text = self._custom_file_parser(request_url, text, logger)
        self._statistics.add_parsed()
        return text

    def set_url_validator(self, url_validator):
        self._custom_url_validator = url_validator

    def set_file_parser(self, parser):
        self._custom_file_parser = parser
