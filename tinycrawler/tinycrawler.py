import multiprocessing
import os
from multiprocessing.managers import BaseManager

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

    def __init__(self, directory="downloaded_websites"):

        if not os.path.exists(directory):
            os.makedirs(directory)

        self._tinycrawler_manager = TinyCrawlerManager()
        self._tinycrawler_manager.start()

        self._logger = self._tinycrawler_manager.Log(directory)
        self._statistics = self._tinycrawler_manager.Statistics()

        self._urls = self._tinycrawler_manager.DictJob(
            "urls", self._statistics, self._logger)
        files = self._tinycrawler_manager.Job("files", self._statistics)
        graph = self._tinycrawler_manager.Job("graph", self._statistics)
        self._proxies = self._tinycrawler_manager.ProxyJob(self._statistics)

        self._file_parser = FileParser(
            path=directory,
            jobs=files,
            statistics=self._statistics,
            logger=self._logger
        )

        self._url_parser = UrlParser(
            path=directory,
            jobs=graph,
            urls=self._urls,
            statistics=self._statistics,
            logger=self._logger
        )

        Downloader(
            urls=self._urls,
            proxies=self._proxies,
            files=files,
            graph=graph,
            statistics=self._statistics,
            logger=self._logger
        )

        self._cli = Cli(self._statistics, self._logger)

    def run(self, seed):
        self._cli.run()
        if isinstance(seed, str):
            self._urls.put(seed)
        elif isinstance(seed, list):
            [self._urls.put(s) for s in seed]
        else:
            raise ValueError("The given seed is not valid.")
        self._cli.join()

    def set_url_validator(self, url_validator):
        self._url_parser.set_url_validator(url_validator)

    def load_proxies(self, test_url, path):
        self._proxies.set_test_url(test_url)
        self._proxies.load(path)

    def set_proxy_timeout(self, timeout):
        self._proxies.set_proxy_timeout(timeout)

    def set_url_extractor(self, file_parser):
        self._url_parser.set_url_extractor(file_parser)

    def set_file_parser(self, file_parser):
        self._file_parser.set_file_parser(file_parser)