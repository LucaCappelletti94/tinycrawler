import time
from multiprocessing import cpu_count

class downloader(process_handler):

    _headers =  {
        'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/45.0.2454.101 Safari/537.36'),
    }

    def __init__(self, urls, proxies, files, logger, statistics):
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
                    request = requests.get(url, headers=self._headers)
                else:
                    request = requests.get(url, headers=self._headers, proxies = proxy["urls"])
                if not self._request_is_binary(request):
                    self._files.put(request.text)
                break
            except Exception as e:
                max_attempts -= 1
                time.sleep(0.5)

        if max_attempts==0:
            self._logger.log("Unable to download webpage at %s"%url)

    def run(self):
        for i in range(cpu_count()*4):
            super().process("downloader n. %s"%(i), self._download)
        super().run()