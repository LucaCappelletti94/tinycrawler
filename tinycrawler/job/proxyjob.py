"""Handle ProxyJob dispatching with timeouts."""
import json
import os
from multiprocessing import Pool, cpu_count
from queue import Empty
from time import sleep, time

from requests import get as require
from requests.exceptions import (ConnectionError, SSLError, Timeout,
                                 TooManyRedirects)

from ..log import Log
from ..statistics import Statistics
from .job import Job


class ProxyJob(Job):
    """Handle Dic ProxyJob dispatching with timeouts."""

    LOCAL = None
    HEADERS = {
        'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/45.0.2454.101 Safari/537.36'),
    }
    CONNECTION_TIMEOUT = 5
    PROXY_TIMEOUT = 2
    CACHE_LIFETIME = 2 * 24 * 60 * 60
    CACHE_FILENAME = "tmp_tested_proxy.json"

    def __init__(self, logger: Log, statistics: Statistics):
        """Handle Dic ProxyJob dispatching with timeouts."""
        super().__init__("proxies", "proxy", logger, statistics)
        self.__put(self.LOCAL)
        self._test_url = None
        self._path = None

    def __get(self):
        """Private get method for ProxyJob that handle timestamp."""
        self._statistics.add("processes", "Downloader waiting proxies")
        while True:
            try:
                proxy = super().get()
                break
            except Empty:
                sleep(0.1)
        self._statistics.remove("processes", "Downloader waiting proxies")
        self._statistics.add(self._name, "Sleeping proxies")
        sleep(max(0, self.PROXY_TIMEOUT + proxy["timestamp"] - time()))
        self._statistics.remove(self._name, "Sleeping proxies")
        return proxy["data"]

    def get(self):
        """Disable get on ProxyJob."""
        raise NotImplementedError("Use 'use' method instead of get!")

    def __put(self, value):
        """Private put method for ProxyJob that handle timestamp."""
        super().put({
            "data": value,
            "timestamp": time()
        })

    def put(self, value):
        """Disable put on ProxyJob."""
        raise NotImplementedError("Use 'use' method instead of put!")

    def use(self, url):
        """Download page at given url using a proxy."""
        proxy = self.__get()
        result = self._require(url, proxy)
        self.__put(proxy)
        return result

    def _cache_is_valid(self):
        return os.path.getctime(self.CACHE_FILENAME) > time() - self.CACHE_LIFETIME

    def _is_cached(self):
        return os.path.exists(self.CACHE_FILENAME) and self._cache_is_valid()

    def _load_cache(self):
        with open(self._path, 'r') as f:
            proxies = json.load(f)
        [self.__put(proxy) for proxy in proxies]

    def _run_tests(self):
        with open(self._path, 'r') as f:
            proxies_data = json.load(f)

        self._statistics.set(self._name, "Testing proxies on", self._test_url)

        tmp = []
        n = len(proxies_data)

        self._statistics.set(
            self._name, "Total proxies to test", n)

        for i, proxy_data in enumerate(proxies_data):
            self._logger.log(
                "Testing proxy {i}/{n} with data:{data}.".format(
                    i=i, n=n, data=proxy_data))
            proxy = self._test_proxy(proxy_data)
            self._logger.log(
                "Test {i}/{n} had result {result}.".format(
                    i=i, n=n, result=bool(proxy)))
            self._statistics.add(
                self._name, "Tested proxies")
            if proxy:
                tmp.append(proxy)
                self.__put(proxy)
                self._statistics.add(
                    self._name, "Total proxies")
            else:
                self._statistics.add(
                    self._name, "Failed proxies")

        with open(self.CACHE_FILENAME, "w") as f:
            json.dump(tmp, f)

    def load(self):
        """Load and test the proxies in provided path."""
        self._logger.log(
            "Starting to load proxies from {path}.".format(path=self._path))
        if not self._path:
            return None

        if self._is_cached():
            self._load_cache()
        else:
            self._run_tests()
        self._statistics.set(self._name, "Total proxies", self.len())

    def _test_proxy(self, proxy_data):
        """Return proxy that pass connection test."""
        proxy = self._proxy_data_to_proxy(proxy_data)
        if self._require(self._test_url, proxy):
            return proxy
        return None

    def _require(self, url, proxy):
        """Download given url using given proxy."""
        try:
            return require(url,
                           proxies=proxy,
                           headers=self.HEADERS,
                           timeout=self.CONNECTION_TIMEOUT
                           )
        except (ConnectionError, Timeout, SSLError, TooManyRedirects):
            return None

    def _proxy_data_to_proxy(self, proxy_data):
        """Return proxy urls obtained from proxy data."""
        support = proxy_data["support"]
        url = "://{ip}:{port}".format(**proxy_data)

        proxy = {}

        for protocol in ["http", "https"]:
            if support[protocol]:
                proxy.update({
                    protocol: protocol + url
                })

        for protocol in ["socks4", "socks5"]:
            if support[protocol]:
                address = protocol + url
                proxy.update({
                    "https": address,
                    "http": address,
                })

        return proxy

    def set_proxy_timeout(self, proxy_timeout):
        """"Set the test server."""
        self.PROXY_TIMEOUT = proxy_timeout

    def set_test_url(self, test_server):
        """"Set the test server."""
        self._test_url = test_server

    def set_proxy_path(self, path):
        """"Set the test server."""
        self._path = path
