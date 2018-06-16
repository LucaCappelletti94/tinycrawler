import json
import os

from .process_handler import ProcessHandler


class Parser(ProcessHandler):

    def __init__(self, path, name, jobs, statistics, logger):
        super().__init__(name, jobs, statistics, logger)
        self._path = path
        self._file_number = 0
        self._counter = 0
        if not os.path.exists(path):
            os.makedirs(path)
        self._bind_jobs()

    def _target(self, job):
        """Parse the downloaded files, cleans them and extracts urls"""
        request_url, html = job

        filename = hash(request_url.encode('utf-8'))
        content = self._parser(request_url, html, self._logger)
        if content is not None:
            self._write(filename, {
                "url": request_url,
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

    def _parser(self, request_url, html, logger):
        raise NotImplementedError
