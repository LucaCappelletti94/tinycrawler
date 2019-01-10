"""Creates a structure to hold proxies."""
from ..expirables import Proxy, ExpirablesQueue, Domain
from ..utils import ProxyData, Printable
from typing import Dict
import json


class Proxies(Printable):
    """Creates a structure to hold proxies."""

    def __init__(self, **kwargs):
        """Creates a structure to hold proxies.
            path:str, path from where to load the proxies.
        """
        path = kwargs.get("path", None)
        self._proxies = ExpirablesQueue()
        if path:
            self._load_proxies(path)

    def _load_proxies(self, path):
        with open(path, "r") as f:
            for data in json.load(f):
                self.add(
                    Proxy(ProxyData(data=data))
                )

    def pop(self, domain: Domain = None)->Proxy:
        """Get a valid proxy for given domain."""
        assert isinstance(domain, Domain)
        return self._proxies.pop(domain=domain)

    def add(self, proxy: Proxy)->Proxy:
        """Add given proxy to proxies, disabling domain test."""
        assert isinstance(proxy, Proxy)
        return self._proxies.add(proxy, domain=None)

    def ___repr___(self)->Dict:
        """Return a dictionary representation of object."""
        return self._proxies.___repr___()
