"""Handle ProxyJob dispatching with timeouts."""
import json
from multiprocessing import Pool, cpu_count
from queue import Empty
from time import sleep, time

from requests import get as require
from requests.exceptions import ConnectionError, SSLError, Timeout

from .job import Job


class ProxyJob(Job):
    """Handle Dic ProxyJob dispatching with timeouts."""

    LOCAL = None
    HEADERS = {
        'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/45.0.2454.101 Safari/537.36'),
    }
    WORKERS = cpu_count() * 4
    CONNECTION_TIMEOUT = 10
    PROXY_TIMEOUT = 2

    def __init__(self, statistics):
        """Handle Dic ProxyJob dispatching with timeouts."""
        super().__init__("proxies", statistics)
        self.__put(self.LOCAL)
        self._test_url = None
        self._statistics.set(self._name, "Total proxies", self.len())

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

    def _put_statistics(self):
        self._put_update_add_statistics()

    def put(self, value):
        """Disable put on ProxyJob."""
        raise NotImplementedError("Use 'use' method instead of put!")

    def use(self, url):
        """Download page at given url using a proxy."""
        proxy = self.__get()
        result = self._require(url, proxy)
        self.__put(proxy)
        return result

    def load(self, path):
        """Load and test the proxies in given file."""
        with open(path, 'r') as f:
            proxies_data = json.load(f)

        with Pool(self.WORKERS) as p:
            [self._put(x) for x in p.imap(self._test_proxy, proxies_data) if x]
        p.join()

        self._statistics.set(self._name, "Total proxies", self.len())

    def _test_proxy(self, proxy_data):
        """Return proxy that pass connection test."""
        proxy = self._proxy_data_to_proxy(proxy_data)
        if self._require(self._test_url, proxy):
            return proxy
        return False

    def _require(self, url, proxy):
        """Download given url using given proxy."""
        try:
            params = {
                "proxies": proxy,
                "headers": self.HEADERS,
                "timeout": self.CONNECTION_TIMEOUT
            }
            return require(url, params)
        except (ConnectionError, Timeout, SSLError):
            return None

    def _proxy_data_to_proxy(self, proxy_data):
        """Return proxy urls obtained from proxy data."""
        support = proxy_data["support"]
        url = "://%s:%s" % (proxy_data["ip"], proxy_data["port"])

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
