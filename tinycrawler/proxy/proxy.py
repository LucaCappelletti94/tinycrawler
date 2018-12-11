from typing import Dict, Callable
from time import time
from ..eta import Eta
from ..domains_eta import DomainsEta
from ..utils import get_domain
from ..robots import Robots
from collections import defaultdict


class Proxy:

    def __init__(
            self,
            data: Dict,
            max_failure_rate: float,
            proxy_timeout: float,
            domains_timeout: float,
            custom_domains_timeout: Callable[[str], float],
            robots: Robots):
        self._data = self._data_to_working_proxy(data)
        self._eta = Eta(proxy_timeout)
        self._max_failure_rate = max_failure_rate
        self._domains_eta = DomainsEta(
            domains_timeout, custom_domains_timeout, robots)
        self._in_use = False
        self._domains = defaultdict({
            "usages": 0,
            "successes": 0,
            "in_use": False
        })

    def _data_to_working_proxy(self, data: Dict):
        if data is None:
            return None
        return {protocol:  "{protocol}://{ip}:{port}".format(protocol=protocol, ip=data["ip"], port=data["port"]) for key, protocol in {
            "http": "http",
            "https": "https",
            "socks4": "https",
            "socks5": "https"
        }.items() if data["support"][key]}

    def data(self):
        return self._data

    def used(self, success: bool, url: str):
        domain = get_domain(url)
        self._domains[domain]["successes"] += success
        self._domains[domain]["usages"] += 1
        self._domains[domain]["in_use"] = False
        self._domains_eta.add(url)
        self._eta.add()

    def use(self, url: str):
        """Set current proxy as in use for given url domain."""
        self._domains[get_domain(url)]["in_use"] = True
        self._in_use = True

    def _currently_used(self)->bool:
        return self._in_use

    def can_use(self, url: str)->bool:
        """Return bool representing if current proxy is used for given url domain."""
        domain = get_domain(url)
        failure_rate = 1 - \
            self._domains[domain]["successes"]/self._domains[domain]["usages"]
        return not self._currently_used() and not self._domains[domain]["in_use"] and failure_rate < self._max_failure_rate

    def get_wait_time(self, url: str)->float:
        """Return time to be waited to start downloading from given url."""
        return max(self._eta.get_wait_time(), self._domains_eta.get_wait_time(url))

    def wait_for(self, value):
        self._domains_eta.wait_for(value)
        self._eta.wait_for()
