import hashlib
import json
import os
import re
from multiprocessing import cpu_count
from urllib.parse import urljoin, urlparse

from validators import url as valid

from .parser import Parser


class UrlParser(Parser):

    def __init__(self, path, jobs, urls):
        super().__init__(path + "/graph", "urls parser", jobs)
        self._regex = re.compile(r"href=\"([^\"#]+)\"")
        self._val = self._tautology
        self._urls = urls
        self._url_extractor = self._default_url_extractor

    def _tautology(self, url):
        return True

    def _default_url_extractor(self, response, urls, logger):
        url = response.url
        for partial_link in re.findall(self._regex, response.text):
            link = urljoin(url, partial_link)
            if valid(link) and self._val(link):
                urls.put(link)

    def _parser(self, response, logger):
        self._url_extractor(response, self._urls, logger)

    def set_validator(self, url_validator):
        """Set custom url validator."""
        self._val = url_validator

    def set_url_extractor(self, url_extractor):
        """Set custom url extractor."""
        self._url_extractor = url_extractor
