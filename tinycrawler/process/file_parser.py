from .parser import Parser
from ..log import Log
from requests import Response
from ..statistics import Statistics
from typing import Callable


class FileParser(Parser):

    def __init__(self, path, jobs):
        super().__init__(
            "{path}/website".format(path=path), "files parser", jobs)
        self._parser = self._default_parser

    def _default_parser(self, response: Response, logger: Log, statistics: Statistics)->str:
        """Parse downloaded page into document to be saved.
            response: 'Response', response object from requests.models.Response
            logger: 'Log', a logger to log eventual errors or infos

            Return None if the page should not be saved.
        """
        return response.text

    def set_file_parser(self, file_parser: Callable[[Response, Log, Statistics], str]):
        """Set custom file parser."""
        self._parser = file_parser
