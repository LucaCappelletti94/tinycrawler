from multiprocessing import cpu_count

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
        self._retry_policy = self._default_retry_policy

    def _default_retry_policy(self, status):
        """Define what to do in case of error."""
        return False

    def enough(self, c):
        return super().enough(c) or self._proxies.len() <= self.alives()

    def set_retry_policy(self, retry_policy):
        """Set retry policy."""
        self._retry_policy = retry_policy

    def _has_content_type(self, headers):
        return 'content-type' in headers

    def _is_text(self, headers):
        return 'text/html' in headers['content-type']

    def _response_is_binary(self, headers):
        return self._has_content_type(headers) and not self._is_text(headers)

    def _target(self, url):
        """Tries to download an url with a proxy n times"""
        attempts = 0

        while attempts < self.MAX_ATTEMPTS:
            response = self._proxies.use(url)
            if response is None:
                attempts += 1
                continue

            status = response.status_code

            if self._response_is_binary(response.headers):
                self._statistics.add("error", "binary files")
                break

            if status == self.SUCCESS_STATUS:
                self._files.put(response)
                self._graph.put(response)
                break
            self._statistics.add(
                "error", "error code {status}".format(status=status))
            if self._retry_policy(status):
                attempts += 1
                continue
            break

        if attempts == self.MAX_ATTEMPTS:
            self._statistics.add("error", "Maximum attempts")
            self._logger.log(
                "Unable to download webpage at {url}".format(url=url))
