import hashlib
import json
import os

from ..statistics import Speed
from .process_handler import ProcessHandler


class Parser(ProcessHandler):

    def __init__(self, path, name, jobs):
        super().__init__(name, jobs)
        self._path = path
        self._file_number = 0
        self._counter = 0
        self._writing_data_speed = Speed("B")
        if not os.path.exists(path):
            os.makedirs(path)

    def _target(self, response: 'Response'):
        """Parse the downloaded files, cleans them and extracts urls"""
        url = response.url

        filename = hashlib.md5(url.encode('utf-8')).hexdigest()
        content = self._parser(response, self._logger)
        if content is not None:
            self._writing_data_speed.update(len(content))
            self._statistics.set("files", "Writing data speed",
                                 self._writing_data_speed.get_formatted_speed())
            self._write(filename, {
                "url": url,
                "content": content
            })

    def _write(self, filename, content):
        """Parse the downloaded files, cleans them and extracts urls"""
        if self._file_number % 10000 == 0:
            self._counter += 1
            directory = "%s/%s" % (self._path, self._counter)
            if not os.path.exists(directory):
                os.makedirs(directory)

        self._file_number += 1

        path = "%s/%s/%s.json" % (self._path, self._counter, filename)

        with open(path, "w") as f:
            json.dump(content, f)
