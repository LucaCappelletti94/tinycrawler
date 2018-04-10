from urllib.parse import urljoin, urlparse
import validators
import hashlib
from bs4 import BeautifulSoup
from ..process.process_handler import process_handler

class file_parser(process_handler):

    def __init__(self, files, parsed, urls, graph, statistics, logger, timeout):
        super().__init__(statistics, logger)
        self._files = files # Queue of files to be parsed
        self._parsed = parsed # Queue of parsed files
        self._urls = urls # UrlQueue of parsed urls
        self._graph = graph # Queue of urls per file
        self._timeout = timeout
        self._custom_file_parser = lambda soup: soup
        self._custom_url_validator = lambda url: True
        self._total_urls = 0
        self._done_urls = 0

    def _valid_url(self, url):
        return validators.url(url)

    def _is_url_downloadable(self, url):
        return self._custom_url_validator(url) and not self._urls.contains(url)

    def _extract_valid_urls(self, request_url, soup):
        urls = []
        for link in soup.find_all('a', href=True):
            url = urljoin(request_url, link["href"])
            if self._valid_url(url):
                urls.append(url)
                if self._is_url_downloadable(url):
                    self._urls.put(url)
                    self._total_urls += 1
        return urls

    def _parse(self):
        """Parse the downloaded files, cleans them and extracts urls"""
        request_url, file = self._files.get(timeout=self._timeout)
        soup = BeautifulSoup(file, 'lxml')
        filename = hashlib.md5(urlparse(request_url).path.encode('utf-8')).hexdigest()
        self._parsed.put((filename,{
            "url": request_url,
            "content": str(self._custom_file_parser(soup))
        }))
        self._graph.put((filename,{
            "incoming": request_url,
            "outgoing": self._extract_valid_urls(request_url, soup)
        }))

        self._done_urls += 1

        self._statistics.set_done(self._done_urls)
        self._statistics.set_total(self._total_urls)

    def set_url_validator(self, custom_url_validator):
        """Sets the user defined url parser"""
        self._custom_url_validator = custom_url_validator

    def set_custom_file_parser(self, custom_file_parser):
        """Sets the user defined file parser"""
        self._custom_file_parser = custom_file_parser

    def run(self):
        """Starts the parser"""
        super().process("parser", self._parse)
        super().run()