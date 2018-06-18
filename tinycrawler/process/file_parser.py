import hashlib
import json
import os
from urllib.parse import urljoin, urlparse

from validators import url

from .parser import Parser


class FileParser(Parser):

    def __init__(self, path, jobs):
        super().__init__(path + "/website", "files parser", jobs)

    def _parser(self, response: 'Response', logger: 'Log')->str:
        """Parse downloaded page into document to be saved.
            response: 'Response', response object from requests.models.Response
            logger: 'Log', a logger to log eventual errors or infos

            Return None if the page should not be saved.
        """
        return response.text

    def set_file_parser(self, file_parser):
        """Set custom file parser."""
        self._parser = file_parser
