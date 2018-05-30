import os
from multiprocessing import Queue
from multiprocessing.managers import BaseManager
from urllib.parse import urlparse

from tinycrawler.cli.cli import cli
from tinycrawler.downloader.downloader import downloader
from tinycrawler.file.file_handler import file_handler
from tinycrawler.log.log import log
from tinycrawler.proxies.proxiesloader import proxiesloader
from tinycrawler.statistics.statistics import statistics
from tinycrawler.triequeue.triequeue import triequeue


class MyManager(BaseManager):
    pass


MyManager.register('statistics', statistics)
MyManager.register('log', log)
MyManager.register('triequeue', triequeue)


class TinyCrawler:

    def __init__(self, seed, directory="downloaded_websites"):

        self._domain = self.domain(seed)
        self._directory = "%s/%s" % (directory, self._domain)

        if not os.path.exists(self._directory):
            os.makedirs(self._directory)

        self._myManager = MyManager()
        self._myManager.start()

        files = [Queue(), Queue()]
        urls = self._myManager.triequeue()
        self._statistics = self._myManager.statistics()
        logger = self._myManager.log(self._directory)

        self._file_handler = file_handler(
            files=files,
            urls=urls,
            path=self._directory,
            statistics=self._statistics,
            logger=logger
        )

        proxies = Queue()
        proxies_loader = proxiesloader(proxy_test_server=seed)
        total = proxies_loader.load(proxies)

        self._statistics.set_total_proxies(total)

        self._downloader = downloader(
            urls=urls,
            proxies=proxies,
            files=files,
            statistics=self._statistics,
            logger=logger
        )

        self._cli = cli(self._statistics, logger)

        self._statistics.add_total(1)

        urls.put(seed)

    def run(self):
        self._cli.run()
        self._downloader.run()
        self._file_handler.run()
        self._file_handler.join()
        self._downloader.join()
        self._statistics.set_done()
        self._cli.join()

    def set_url_validator(self, url_validator):
        self._file_handler.set_url_validator(url_validator)

    def set_file_parser(self, file_parser):
        self._file_handler.set_file_parser(file_parser)

    def domain(self, url):
        return '{uri.netloc}'.format(uri=urlparse(url))
