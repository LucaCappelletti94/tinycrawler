import os
from time import sleep, time
from typing import Callable
from .managers import TinyCrawlerManager
from .utils import get_domain
from .cli import Cli
from .job import FileJob, ProxyJob, UrlJob, RobotsJob
from .log import Log
from .process import Downloader, Parser
from .statistics import Statistics, Time
from bs4 import BeautifulSoup


class TinyCrawler:
    CRYOUTS = 4

    def __init__(self, file_parser: Callable[[str, BeautifulSoup, Log], None], url_validator: Callable[[str, Log], bool], use_cli: bool=True, bloom_filters_capacity: int=1e9, follow_robots_txt: bool=True, proxy_timeout: int=2):

        self._use_cli = use_cli

        self._tinycrawler_manager = TinyCrawlerManager()
        self._tinycrawler_manager.start()
        self._time = Time()

        self._logger = self._tinycrawler_manager.Log()
        self._statistics = self._tinycrawler_manager.Statistics()

        self._urls = self._tinycrawler_manager.UrlJob(
            self._statistics, bloom_filters_capacity)
        self._files = self._tinycrawler_manager.FileJob(self._statistics)
        self._robots = self._tinycrawler_manager.RobotsJob()
        self._proxies = self._tinycrawler_manager.ProxyJob(
            self._statistics, proxy_timeout=proxy_timeout)

        self.parser = Parser(
            jobs=self._files,
            urls=self._urls,
            robots=self._robots,
            file_parser=file_parser,
            url_validator=url_validator,
            statistics=self._statistics,
            logger=self._logger,
            follow_robots_txt=follow_robots_txt)

        self._downloader = Downloader(
            jobs=self._urls,
            proxies=self._proxies,
            files=self._files,
            statistics=self._statistics
        )

        if self._use_cli:
            self._cli = Cli(self._statistics, self._logger)

    def _add_seed(self, seed):
        if isinstance(seed, str):
            seed = [seed]
        self._urls.put(seed)
        self._statistics.set("info", "Working on", get_domain(seed[0]))

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
        self.parser.bind()
        self._downloader.bind()
        self._add_seed(seed)
        self._proxies.load()
        self._sleep_loop()
        self.parser.join()
        self._downloader.join()
        if self._use_cli:
            self._cli.join()

    def load_proxies(self, test_url: str, path: str):
        self._proxies.set_test_url(test_url)
        self._proxies.set_proxy_path(path)
