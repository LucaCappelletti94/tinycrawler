import multiprocessing
import os
import traceback
from multiprocessing.managers import BaseManager
from time import sleep

from .cli import Cli
from .job import DictJob, Job, ProxyJob
from .log import Log
from .process import Downloader, FileParser, UrlParser
from .statistics import Statistics

backup_autoproxy = multiprocessing.managers.AutoProxy


def redefined_autoproxy(token, serializer, manager=None, authkey=None,
                        exposed=None, incref=True, manager_owned=True):
    return backup_autoproxy(token, serializer, manager, authkey,
                            exposed, incref)


multiprocessing.managers.AutoProxy = redefined_autoproxy


class TinyCrawlerManager(BaseManager):
    pass


TinyCrawlerManager.register('Statistics', Statistics)
TinyCrawlerManager.register('Log', Log)
TinyCrawlerManager.register('DictJob', DictJob)
TinyCrawlerManager.register('Job', Job)
TinyCrawlerManager.register('ProxyJob', ProxyJob)


class TinyCrawler:

    def __init__(self, use_cli=False, directory="downloaded_websites"):

        self._use_cli = use_cli
        self._directory = directory

        if not os.path.exists(self._directory):
            os.makedirs(self._directory)

        self._tinycrawler_manager = TinyCrawlerManager()
        self._tinycrawler_manager.start()

        self._logger = self._tinycrawler_manager.Log(self._directory)
        self._statistics = self._tinycrawler_manager.Statistics()

        self._urls = self._tinycrawler_manager.DictJob(
            "urls", self._statistics, self._logger)
        self._files = self._tinycrawler_manager.Job("files", self._statistics)
        self._graph = self._tinycrawler_manager.Job("graph", self._statistics)
        self._proxies = self._tinycrawler_manager.ProxyJob(self._statistics)

        self._start_file_parser()
        self._start_url_parser()
        self._start_downloader()

        if self._use_cli:
            self._cli = Cli(self._statistics, self._logger)

    def _start_file_parser(self):
        self._file_parser = FileParser(
            path=self._directory,
            jobs=self._files
        )
        self._file_parser.set_statistics(self._statistics)
        self._file_parser.set_logger(self._logger)
        self._file_parser.bind()

    def _start_url_parser(self):
        self._url_parser = UrlParser(
            path=self._directory,
            jobs=self._graph,
            urls=self._urls
        )
        self._url_parser.set_statistics(self._statistics)
        self._url_parser.set_logger(self._logger)
        self._url_parser.bind()

    def _start_downloader(self):
        self._downloader = Downloader(
            urls=self._urls,
            proxies=self._proxies,
            files=self._files,
            graph=self._graph
        )
        self._downloader.set_statistics(self._statistics)
        self._downloader.set_logger(self._logger)
        self._downloader.bind()

    def _add_seed(self, seed):
        if isinstance(seed, str):
            self._urls.put(seed)
        elif isinstance(seed, list):
            [self._urls.put(s) for s in seed]
        else:
            raise ValueError("The given seed is not valid.")

    def _sleep_loop(self):
        attempt = 0
        max_attempt = 5
        while True:
            sleep(0.1)
            if self._statistics.is_everything_dead():
                attempt += 1
            if attempt > max_attempt:
                break

    def run(self, seed):
        if self._use_cli:
            self._cli.run()
        self._add_seed(seed)
        self._sleep_loop()
        self._file_parser.join()
        self._url_parser.join()
        self._downloader.join()
        if self._use_cli:
            self._cli.join()

    def set_url_validator(self, url_validator):
        self._url_parser.set_validator(url_validator)

    def load_proxies(self, test_url, path):
        self._proxies.set_test_url(test_url)
        self._proxies.load(path)

    def set_proxy_timeout(self, timeout):
        self._proxies.set_proxy_timeout(timeout)

    def set_url_extractor(self, file_parser):
        self._url_parser.set_url_extractor(file_parser)

    def set_file_parser(self, file_parser):
        self._file_parser.set_file_parser(file_parser)

    def set_retry_policy(self, retry_policy):
        self._downloader.set_retry_policy(retry_policy)
