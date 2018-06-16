import hashlib
import json
import os
from urllib.parse import urljoin, urlparse

from validators import url

from .parser import Parser


class FileParser(Parser):

    def __init__(self, path, jobs):
        super().__init__(path, "file parser", jobs)
        path = path + "/website"

    def _parser(self, request_url, text, logger):
        return text

    def set_file_parser(self, file_parser):
        """Set custom file parser."""
        self._parser = file_parser
