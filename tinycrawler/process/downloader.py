from multiprocessing import cpu_count, Event, Value
from .process_handler import ProcessHandler
from ..statistics import Statistics
from user_agent import generate_user_agent
from typing import Callable, Dict
import requests
from time import sleep, time
from queue import Empty
from ..proxy import Local, Proxy, ProxyQueue
from requests import Response
from multiprocessing.queues import Queue
from ..urls import Urls
from ..managers import TinyCrawlerManager
from requests.exceptions import (ConnectionError, SSLError, Timeout,
                                 TooManyRedirects)


class Downloader(ProcessHandler):
    def __init__(
            self, process_spawn_event: Event, process_callback_event: Event, pages_number: Value, urls_number: Value,
            urls: Urls, manager: TinyCrawlerManager, responses: Queue, statistics: Statistics, connection_timeout: float,
            custom_connection_timeout: Callable[[str], float], maximal_failure_proxy_rate: float, download_attempts: int,
            cooldown_time_beetween_download_attempts: float):

        super().__init__("downloader", statistics, process_spawn_event)
        self._urls = urls
        self._pages_number = pages_number
        self._urls_number = urls_number
        self._maximal_failure_proxy_rate = maximal_failure_proxy_rate
        self._process_callback_event = process_callback_event
        self._responses = responses
        self._timeout = connection_timeout
        self._download_attempts = download_attempts
        self._cooldown_time_beetween_download_attempts = cooldown_time_beetween_download_attempts
        self._proxies = ProxyQueue()

        if custom_connection_timeout is not None:
            self._connection_timeout = custom_connection_timeout
        else:
            self._connection_timeout = self._default_connection_timeout

        self.MAXIMUM_PROCESSES = cpu_count() * 4

    def _has_content_type(self, headers):
        return 'content-type' in headers

    def _is_text(self, headers):
        return 'text/html' in headers['content-type']

    def _response_is_binary(self, headers):
        return self._has_content_type(headers) and not self._is_text(headers)

    def _default_connection_timeout(self, url: str)->float:
        return self._timeout

    def _generate_headers(self):
        return {
            'user-agent': generate_user_agent()
        }

    def _handle_successful_download(self, response: Response):
        if self._response_is_binary(response.headers):
            self._statistics.add("error", "binary responses")
        elif response.status_code == 200:
            self._responses.put(response)
            self._pages_number.value += 1
            self._statistics.add("Pages", "Total Pages")
            self._process_callback_event.set()
        else:
            self._statistics.add(
                "error", "error code {status}".format(status=response.status_code))

    def _download(self, proxy: Proxy, url: str)->Response:
        try:
            return requests.get(url,
                                proxies=proxy.data(),
                                headers=self._generate_headers(),
                                timeout=self._connection_timeout(url)
                                )
        except (ConnectionError, Timeout, SSLError, TooManyRedirects):
            return None

    def _get_proxy(self, url: str)->Proxy:
        try:
            proxy = self._proxies.get_nowait()
        except Empty:
            proxy = self._local
        proxy.wait_for(url)
        return proxy

    def _enough(self, active_processes):
        return active_processes*20 > self._urls_number.value

    def _get_job(self):
        url, local = self._urls.get(self._local.unripe())
        if url is None:
            raise Empty
        self._urls_number.value -= 1
        self._statistics.set("Urls", "Remaining Urls",
                                     self._urls_number.value)
        if local:
            return self._local, url
        return self._get_proxy(url), url

    def _target(self, proxy: Proxy, url: str):
        """Tries to download an url with a proxy n times"""
        for attempts in range(self._download_attempts):
            response = self._download(proxy, url)
            proxy.used(bool(response), url)
            if not proxy.is_local() and proxy.failure_rate() < self._maximal_failure_proxy_rate:
                self._proxies.put(proxy)
            if response is None:
                sleep(self._cooldown_time_beetween_download_attempts)
                proxy = self._get_proxy(url)
                continue
            self._handle_successful_download(response)
            break
        if attempts + 1 == self._download_attempts:
            self._statistics.add("error", "Maximum attempts")
