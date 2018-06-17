import hashlib
import json
import os
import re
from multiprocessing import cpu_count
from urllib.parse import urljoin, urlparse

from validators import url

from .parser import Parser


class UrlParser(Parser):

    def __init__(self, path, jobs, urls):
        super().__init__(path + "/graph", "url parser", jobs)
        self._regex = re.compile(r"href=[\"']([^\"#\']+)[\"']")
        self._val = self._tautology
        self._urls = urls

    def _tautology(self, url):
        return True

    def _url_extractor(self, request_url, text, urls, logger):
        for partial_link in re.findall(self._regex, text):
            link = urljoin(request_url, partial_link)
            if url(link) and self._val(link):
                urls.put(link)

    def _parser(self, request_url, text, logger):
        self._url_extractor(request_url, text, self._urls, logger)

    def set_validator(self, url_validator):
        """Set custom url validator."""
        self._val = url_validator

    def set_url_extractor(self, url_extractor):
        """Set custom url extractor."""
        self._url_extractor = url_extractor
