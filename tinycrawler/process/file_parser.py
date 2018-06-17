import hashlib
import json
import os
from urllib.parse import urljoin, urlparse

from validators import url

from .parser import Parser


class FileParser(Parser):

    def __init__(self, path, jobs):
        super().__init__(path + "/website", "file parser", jobs)

    def _parser(self, request_url: str, text: str, logger: 'Log')->str:
        """Parse downloaded page into document to be saved.
            request_url: str, the url of given downloaded page
            text: str, the content of the page
            logger: 'Log', a logger to log eventual errors or infos

            Return None if the page should not be saved.
        """
        return text

    def set_file_parser(self, file_parser):
        """Set custom file parser."""
        self._parser = file_parser
