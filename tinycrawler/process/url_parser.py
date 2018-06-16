import hashlib
import json
import os
import re
from urllib.parse import urljoin, urlparse

from validators import url

from .parser import Parser


class UrlParser(Parser):

    def __init__(self, path, jobs, urls, statistics, logger):
        self._regex = re.compile(r"href=[\"']([^\"#\']+)[\"']")
        self._val = self._tautology
        self._urls = urls
        path = path + "/graph"
        super().__init__(path, "url parser", jobs, statistics, logger)

    def _tautology(self, url):
        return True

    def _url_extractor(self, request_url, text, urls, logger):
        for partial_link in re.findall(self._regex, text):
            link = urljoin(request_url, partial_link)
            if url(link) and self._val(link) and not self._urls.contains(link):
                urls.put(link)

    def _parser(self, request_url, text, logger):
        self._url_extractor(request_url, text, self._urls, logger)

    def set_validate(self, url_validator):
        """Set custom url validator."""
        self._val = url_validator

    def set_url_extractor(self, url_extractor):
        """Set custom url extractor."""
        self._url_extractor = url_extractor
