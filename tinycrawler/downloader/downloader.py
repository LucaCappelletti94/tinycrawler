import time
from multiprocessing import cpu_count

from requests import get
from requests.exceptions import ConnectionError, SSLError, Timeout

from ..process.process_handler import process_handler


class Downloader(process_handler):

    _headers = {
        'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/45.0.2454.101 Safari/537.36'),
    }

    def __init__(self, urls, proxies, files, logger, statistics):
        super().__init__(statistics, logger)
        self._urls = urls
        self._proxies = proxies
        self._files = files
        self._logger = logger
        self._statistics = statistics

    def _request_is_binary(self, request):
        return 'text/html' not in request.headers['content-type']

    def _download(self):
        """Tries to download an url with a proxy n times"""

        self._statistics.add_process_waiting_url()
        url = self._urls.get(timeout=60)
        self._statistics.remove_process_waiting_url()

        max_attempts = 80
        success = False

        while max_attempts > 0:
            self._statistics.add_process_waiting_proxy()
            proxy = self._proxies.get(timeout=60)
            if proxy["start"] != 0:
                timeout = max(0, 2 - (time.time() - proxy["start"]))
                time.sleep(timeout)
            self._statistics.remove_process_waiting_proxy()
            try:
                if proxy["local"]:
                    request = get(url, headers=self._headers)
                else:
                    request = get(url, headers=self._headers,
                                  proxies=proxy["urls"], timeout=10)
                success = True
                if request.status_code == 403:
                    success = False
            except (ConnectionError, Timeout, SSLError):
                pass
            except Exception as e:
                self._logger.log("Error while downloading %s, %s" % (url, e))

            proxy["start"] = time.time()
            self._statistics.add_free_proxy()
            self._proxies.put(proxy)

            if success:
                break

            max_attempts -= 1

        if success:
            if self._request_is_binary(request):
                self._statistics.add_binary_request()
            elif request.status_code == 200:
                self._statistics.add_downloaded(len(request.text))
                for file in self._files:
                    file.put((url, request.text))
            else:
                self._statistics.add_error_code(request.status_code)
        else:
            self._statistics.add_failed()
            self._logger.log("Unable to download webpage at %s" % url)

    def run(self):
        self._download()
        self._statistics.bite()
        processes_number = cpu_count() * 8 * 3
        for i in range(processes_number):
            super().process("downloader", "downloader n. %s" % (i), self._download)
        self._statistics.set_total_downloaders(processes_number)
        super().run()
