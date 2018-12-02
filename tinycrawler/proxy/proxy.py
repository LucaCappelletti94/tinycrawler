from typing import Dict, Callable
from time import time
from ..ETA import ETA
from ..domains_ETA import DomainsETA
from ..robots import Robots
import traceback


class Proxy:
    def __init__(self, data: Dict, proxy_timeout: float, domains_timeout: float, custom_domains_timeout: Callable[[str], float], follow_robots_txt: bool, robots: Robots):
        self._data = self._data_to_working_proxy(data)
        self._ETA = ETA(proxy_timeout)
        self._domains_ETA = DomainsETA(
            domains_timeout, custom_domains_timeout, follow_robots_txt, robots)
        self._usages = self._successes = 0

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

    def success_rate(self)->float:
        return self._usages / self._successes

    def used(self, success: bool, url: str):
        self._usages += 1
        self._successes += success
        self._domains_ETA.add(url)
        self._ETA.add()

    def unripe(self):
        return self._domains_ETA.unripe()

    def wait_for(self, value):
        self._domains_ETA.wait_for(value)
        self._ETA.wait_for()

    def is_local(self):
        return False
