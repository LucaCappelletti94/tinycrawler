from ..expirables import Proxy, ExpirablesQueue, Domain
from ..utils import ProxyData, Printable
from typing import Dict
import json


class Proxies(Printable):
    def __init__(self, **kwargs):
        path = kwargs.get("path", None)
        self._proxies = ExpirablesQueue(Proxy)
        if path:
            self._load_proxies(path)

    def _load_proxies(self, path):
        with open(path, "r") as f:
            [
                self.add(
                    Proxy(ProxyData(data=data))
                ) for data in json.load(f)
            ]

    def pop(self, domain: Domain)->Proxy:
        return self._proxies.pop(domain=domain)

    def add(self, proxy: Proxy)->Proxy:
        return self._proxies.add(proxy, domain=None)

    def ___repr___(self)->Dict:
        return self._proxies.___repr___()
