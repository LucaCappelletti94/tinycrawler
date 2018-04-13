import hashlib
import os
import json
from ..process.process_handler import process_handler

class file_parser(process_handler):

    def __init__(self, input_queue, statistics, logger, path, timeout):
        super().__init__(statistics, logger)
        self._input_queue = input_queue # Queue of files to be parsed
        self._timeout = timeout
        self._logger = logger
        self._path = path
        self._file_number = 0
        self._counter = 0

        if not os.path.exists(path):
            os.makedirs(path)

    def _parse(self):
        """Parse the downloaded files, cleans them and extracts urls"""
        request_url, file = self._input_queue.get(timeout=self._timeout)
        filename = hashlib.md5(request_url.encode('utf-8')).hexdigest()
        content = self._custom_parser(request_url, file, self._logger)
        if content != None:
            self._write(filename,{
                "url": request_url,
                "content": content
            })

    def _write(self, filename, content):
        """Parse the downloaded files, cleans them and extracts urls"""
        if self._file_number%10000 == 0:
            self._counter +=1
            directory = "%s/%s"%(self._path, self._counter)
            if not os.path.exists(directory):
                os.makedirs(directory)

        self._file_number +=1

        with open("%s/%s/%s.json"%(self._path, self._counter, filename), "w") as f:
            json.dump(content, f)

    def set_custom_parser(self, custom_parser):
        """Sets the user defined url parser"""
        self._custom_parser = custom_parser

    def run(self, target):
        """Starts the parser"""
        super().process("%s parser"%target, "%s parser"%target, self._parse)
        super().run()