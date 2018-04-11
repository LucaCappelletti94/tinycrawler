import hashlib
from ..process.process_handler import process_handler
from bs4 import BeautifulSoup

class file_parser(process_handler):

    def __init__(self, input_queue, output_queue, statistics, logger, timeout):
        super().__init__(statistics, logger)
        self._input_queue = input_queue # Queue of files to be parsed
        self._output_queue = output_queue # Queue of parsed files
        self._timeout = timeout
        self._custom_parser = lambda request_url, soup: str(soup)

    def _parse(self):
        """Parse the downloaded files, cleans them and extracts urls"""
        request_url, file = self._input_queue.get(timeout=self._timeout)
        file_soup = BeautifulSoup(file, 'lxml')
        filename = hashlib.md5(request_url.encode('utf-8')).hexdigest()
        self._output_queue.put((filename,{
            "url": request_url,
            "content": self._custom_parser(request_url, file_soup)
        }))

    def set_custom_parser(self, custom_parser):
        """Sets the user defined url parser"""
        self._custom_parser = custom_parser

    def run(self, target):
        """Starts the parser"""
        super().process("%s parser"%target, self._parse)
        super().run()