import queue
import time
from multiprocessing import cpu_count

from requests import get
from requests.exceptions import ConnectionError, SSLError, Timeout

from .process_handler import ProcessHandler


class Downloader(ProcessHandler):
    MAX_ATTEMPTS = 50
    SUCCESS_STATUS = 200

    def __init__(self, urls, proxies, files, graph):
        super().__init__("downloader", urls)
        self._proxies = proxies
        self._files = files
        self._graph = graph
        self.MAXIMUM_PROCESSES = cpu_count() * 4

    def _retry(self, status):
        """Define what to do in case of error."""
        return False

    def enough(self, c):
        return super().enough(c) or self._proxies.len() <= self.alives()

    def set_retry_policy(self, retry_policy):
        """Set retry policy."""
        self._retry = retry_policy

    def _request_is_binary(self, request):
        return 'text/html' not in request.headers['content-type']

    def _target(self, url):
        """Tries to download an url with a proxy n times"""
        attempts = 0

        while attempts < self.MAX_ATTEMPTS:
            request = self._proxies.use(url)
            if request is None:
                attempts += 1
                continue

            status = request.status_code

            if self._request_is_binary(request):
                self._statistics.add("error", "binary files")
                break

            if status == self.SUCCESS_STATUS:
                self._files.put((url, request.text))
                self._graph.put((url, request.text))
                break
            self._statistics.add("error", "error code %s" % status)
            if self._retry(status):
                attempts += 1
                continue
            break

        if attempts == self.MAX_ATTEMPTS:
            self._statistics.add("error", "Maximum attempts")
            self._logger.log("Unable to download webpage at %s" % url)
