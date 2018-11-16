import os
from time import sleep, time
from typing import Callable
from .managers import TinyCrawlerManager
from .utils import get_domain
from .cli import Cli
from .job import FileJob, ProxyJob, UrlJob, RobotsJob
from .log import Log
from .process import Downloader, FileParser, UrlParser
from .statistics import Statistics, Time


class TinyCrawler:
    CRYOUTS = 4

    def __init__(self, use_cli: bool=True, directory: str="downloaded_websites", bloom_filters_number: int=3, bloom_filters_capacity: int=1e9, use_beautiful_soup: bool=False, follow_robots_txt: bool=True):

        self._use_cli = use_cli
        self._directory = directory

        if not os.path.exists(self._directory):
            os.makedirs(self._directory)

        self._tinycrawler_manager = TinyCrawlerManager()
        self._tinycrawler_manager.start()
        self._time = Time()

        self._logger = self._tinycrawler_manager.Log(self._directory)
        self._statistics = self._tinycrawler_manager.Statistics()

        self._urls = self._tinycrawler_manager.UrlJob(
            self._logger, self._statistics, bloom_filters_number, bloom_filters_capacity)
        self._files = self._tinycrawler_manager.FileJob(
            "data extraction", self._logger, self._statistics)
        self._graph = self._tinycrawler_manager.FileJob(
            "urls extraction", self._logger, self._statistics)
        self._robots = self._tinycrawler_manager.RobotsJob(
            self._logger, self._statistics)
        self._proxies = self._tinycrawler_manager.ProxyJob(
            self._logger, self._statistics)

        self._start_file_parser()
        self._start_url_parser(use_beautiful_soup, follow_robots_txt)
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

    def _start_url_parser(self, use_beautiful_soup: bool, follow_robots_txt: bool):
        self._url_parser = UrlParser(
            path=self._directory,
            jobs=self._graph,
            urls=self._urls,
            robots=self._robots,
            use_beautiful_soup=use_beautiful_soup,
            follow_robots_txt=follow_robots_txt
        )
        self._url_parser.set_statistics(self._statistics)
        self._url_parser.set_logger(self._logger)

    def _start_downloader(self):
        self._downloader = Downloader(
            urls=self._urls,
            proxies=self._proxies,
            files=self._files,
            graph=self._graph
        )
        self._downloader.set_statistics(self._statistics)
        self._downloader.set_logger(self._logger)

    def _add_seed(self, seed):
        if isinstance(seed, str):
            self._statistics.set("info", "Working on", get_domain(seed))
            self._urls.put(seed)
        elif isinstance(seed, list):
            self._statistics.set("info", "Working on", get_domain(seed[0]))
            [self._urls.put(s) for s in seed]
        else:
            raise ValueError("The given seed is not valid.")

    def _sleep_loop(self):
        start = time()
        cryouts = 0
        try:
            while True:
                self._statistics.set("time", "Elapsed time",
                                     self._time.seconds_to_string(time() - start))
                sleep(0.5)
                if self._statistics.is_everything_dead():
                    cryouts += 1
                else:
                    cryouts = 0
                if cryouts == self.CRYOUTS:
                    break
        except KeyboardInterrupt:
            pass

    def run(self, seed):
        self._logger.log("Starting crawler.")
        if self._use_cli:
            self._cli.run()
        self._file_parser.bind()
        self._downloader.bind()
        self._url_parser.bind()
        self._add_seed(seed)
        self._proxies.load()
        self._sleep_loop()
        self._file_parser.join()
        self._url_parser.join()
        self._downloader.join()
        if self._use_cli:
            self._cli.join()

    def set_url_validator(self, url_validator: Callable[[str, Log, Statistics], bool]):
        self._url_parser.set_validator(url_validator)

    def load_proxies(self, test_url: str, path: str):
        self._proxies.set_test_url(test_url)
        self._proxies.set_proxy_path(path)

    def set_proxy_timeout(self, timeout: int):
        self._proxies.set_proxy_timeout(timeout)

    def set_file_parser(self, file_parser):
        self._file_parser.set_file_parser(file_parser)

    def set_retry_policy(self, retry_policy):
        self._downloader.set_retry_policy(retry_policy)
