import time
import requests
from multiprocessing import cpu_count
from bs4 import BeautifulSoup
from ..process.process_handler import process_handler

class downloader(process_handler):

    _headers =  {
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

        url = self._urls.get(timeout=60)

        max_attempts = 10

        while max_attempts>0:
            proxy,timeout = self._proxies.get(timeout=60)
            time.sleep(timeout)

            try:
                if proxy["local"]:
                    request = requests.get(url, headers=self._headers, allow_redirects=True)
                else:
                    request = requests.get(url, headers=self._headers, proxies = proxy["urls"], allow_redirects=True)
                if not self._request_is_binary(request) and request.status_code==200:
                    for file_queue in self._files:
                        file_queue.put((url, BeautifulSoup(request.text, 'lxml')))
                break
            except Exception as e:
                max_attempts -= 1

        if max_attempts==0:
            self._statistics.add_failed()
            self._logger.log("Unable to download webpage at %s"%url)

    def run(self):
        for i in range(cpu_count()*8):
            super().process("downloader n. %s"%(i), self._download)
        super().run()