import json
from .proxy import Proxy
from .local import Local
from typing import List, Dict, Callable
from ..robots import Robots
from multiprocessing import Lock


class ProxyQueue:
    def __init__(
            self,
            proxy_path: str,
            proxy_list: List[Dict],
            max_failure_rate: float,
            proxy_timeout: float,
            domains_timeout: float,
            custom_domains_timeout: Callable[[str], float],
            robots: Robots):
        if proxy_list is None:
            proxy_list = []
        if proxy_path is not None:
            with open(proxy_path, "r") as f:
                proxy_list += json.load(f)
        self._proxies = [
            Proxy(data, max_failure_rate, proxy_timeout, domains_timeout, custom_domains_timeout, robots) for data in proxy_list
        ]

        self._proxies.append(
            Local(max_failure_rate, domains_timeout,
                  custom_domains_timeout, robots)
        )
        self._get_lock = Lock()

    def get(self, url: str)->Proxy:
        """Retrieves a valid proxy for given url."""
        time = 0
        first = True
        best = None
        self._get_lock.acquire()
        for proxy in self._proxies:
            proxy_wait_time = proxy.get_wait_time()
            if not proxy.in_use(url) and (first or time > proxy_wait_time):
                time = proxy_wait_time
                best = proxy
                first = False
        self._get_lock.release()
        if best is not None:
            best.wait_for(url)
        else:
            return None
        best.use(url)
        return best
