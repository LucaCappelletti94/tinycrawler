import os
from time import sleep, time
from typing import Callable, List, Dict
from .managers import TinyCrawlerManager
from .utils import get_domain
from .cli import Cli
from .urls import Urls
from .log import Log
from .proxy import Proxy
from .robots import Robots
from .process import Downloader, Parser
from .statistics import Statistics, Time
from multiprocessing import Event, Queue, Value
from bs4 import BeautifulSoup
import json


class TinyCrawler:
    def __init__(
            self, file_parser: Callable[[str, BeautifulSoup, Log], None], url_validator: Callable[[str, Log], bool],
            use_cli: bool=True, bloom_filters_capacity: int=1e9, responses_queue_max_size: int= 10000, download_attempts: int=10, follow_robots_txt: bool=True,
            proxy_timeout: float=10, domains_timeout: float=10, robots_timeout: float=60*60*24, connection_timeout: float=5, cooldown_time_beetween_download_attempts: float=1,
            custom_domains_timeout: Callable[[str], float] = None, custom_connection_timeout: Callable[[str], float] = None,
            parser_library: str="html5lib",
            log_filename: str="crawler.log",
            proxy_path: str = None,
            proxy_list: List[Dict] = None):

        self._use_cli = use_cli

        self._tinycrawler_manager = TinyCrawlerManager()
        self._tinycrawler_manager.register_all()
        self._tinycrawler_manager.start()
        self._time = Time()
        self._close = Event()

        self._logger = self._tinycrawler_manager.Log(log_filename)
        self._statistics = self._tinycrawler_manager.Statistics()
        self._robots = self._tinycrawler_manager.Robots(robots_timeout)
        self._local = self._tinycrawler_manager.Local(
            domains_timeout, custom_domains_timeout, follow_robots_txt, self._robots)

        new_page_event = Event()
        new_url_event = Event()
        self._pages_number = Value('i', 0, lock=False)
        self._urls_number = Value('i', 0, lock=False)

        self._urls = self._tinycrawler_manager.Urls(
            self._statistics, bloom_filters_capacity)
        self._responses = Queue(responses_queue_max_size)
        self._proxies = Queue()
        self._load_proxies(proxy_path, proxy_list, proxy_timeout, domains_timeout,
                           custom_domains_timeout, follow_robots_txt, self._robots)

        self._parser = Parser(
            process_spawn_event=new_page_event,
            process_callback_event=new_url_event,
            pages_number=self._pages_number,
            urls_number=self._urls_number,
            responses=self._responses,
            urls=self._urls,
            robots=self._robots,
            file_parser=file_parser,
            url_validator=url_validator,
            statistics=self._statistics,
            logger=self._logger,
            follow_robots_txt=follow_robots_txt,
            parser_library=parser_library
        )

        self._downloader = Downloader(
            process_spawn_event=new_url_event,
            process_callback_event=new_page_event,
            pages_number=self._pages_number,
            urls_number=self._urls_number,
            urls=self._urls,
            local=self._local,
            proxies=self._proxies,
            responses=self._responses,
            statistics=self._statistics,
            connection_timeout=connection_timeout,
            custom_connection_timeout=custom_connection_timeout,
            download_attempts=download_attempts,
            cooldown_time_beetween_download_attempts=cooldown_time_beetween_download_attempts
        )

        if self._use_cli:
            self._cli = Cli(self._statistics, self._logger, self._close)

    def _add_seed(self, seed):
        if isinstance(seed, str):
            seed = [seed]
        self._urls.put(seed)
        self._urls_number.value += len(seed)
        self._statistics.set("info", "Working on", get_domain(seed[0]))
        self._downloader.add_process()

    def _end_reached(self):
        start = time()
        while True:
            self._statistics.set("time", "Elapsed time",
                                 self._time.seconds_to_string(time() - start))
            sleep(0.5)
            self._downloader.job_event_check()
            self._parser.job_event_check()
            if sum([self._downloader.alive_processes_number(), self._parser.alive_processes_number(), self._urls_number.value, self._pages_number.value]) == 0:
                self._close.set()
                break

    def run(self, seed):
        self._logger.log("Starting crawler.")
        if self._use_cli:
            self._cli.run()
        self._add_seed(seed)
        self._end_reached()
        self._tinycrawler_manager.shutdown()
        self._parser.join()
        self._downloader.join()
        if self._use_cli:
            self._cli.join()

    def _load_proxies(self, proxy_path: str, proxy_list: List[Dict], proxy_timeout: float, domains_timeout: float, custom_domains_timeout: Callable[[str], float], follow_robots_txt: bool, robots: Robots):
        if proxy_list is None:
            proxy_list = []
        if proxy_path is not None:
            with open(proxy_path, "r") as f:
                proxy_list += json.load(f)
        [
            self._proxies.put(Proxy(data, proxy_timeout, domains_timeout, custom_domains_timeout, follow_robots_txt, robots)) for data in proxy_list
        ]
