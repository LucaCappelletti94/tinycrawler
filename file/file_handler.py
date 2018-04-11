from multiprocessing import Queue

from urllib.parse import urljoin, urlparse
import validators

from .file_parser import file_parser
from .file_writer import file_writer

class file_handler:

    def __init__(self, files, urls, path, statistics, logger, timeout = 30):

        parsed = Queue()
        graph = Queue()

        self._file_parser = file_parser(
            input_queue = files[0],
            output_queue = parsed,
            statistics = statistics,
            logger = logger,
            timeout = timeout
        )
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
        self._url_parser.set_custom_parser(self._extract_valid_urls)
        self._file_parser.run()
        self._url_parser.run()
        self._webpages_writer.run()
        self._graph_writer.run()

    def join(self):
        self._url_parser.join()
        self._file_parser.join()
        self._webpages_writer.join()
        self._graph_writer.join()

    def _extract_valid_urls(self, request_url, soup):
        urls = []
        for link in soup.find_all('a', href=True):
            url = urljoin(request_url, link["href"])
            if validators.url(url):
                urls.append(url)
                if self._custom_url_validator(url) and not self._urls.contains(url):
                    self._urls.put(url)
        self._statistics.add_done()
        self._statistics.add_total(len(urls))
        return urls

    def set_url_validator(self, url_validator):
        self._custom_url_validator = url_validator

    def set_file_parser(self, parser):
        self._file_parser.set_custom_parser(parser)