from ..sporadic_sequential_expirable import SporadicSequentialExpirable
from typing import Dict
from ..web import Domain, Url
from ...utils import ProxyData


class Proxy(SporadicSequentialExpirable):
    def __init__(self, domain: Domain, proxy_data: ProxyData, **kwargs):
        super(Proxy, self).__init__(**kwargs)
        self._domain = domain
        self._data = proxy_data
        self._domains = {}

    def is_available(self, url: Url)->bool:
        if not super(Proxy, self).is_available():
            return False
        if url.domain in self._domains:
            return self._domains[url.domain].is_available()
        return True

    @property
    def data(self)->ProxyData:
        return self._data

    @property
    def local(self)->bool:
        return self._data is None

    def use(self, url: Url, **kwargs):
        super(Proxy, self).use(url=url, **kwargs)
        if url.domain not in self._domains:
            self._domains[url.domain] = url.domain
        self._domains[url.domain].use(**kwargs)

    def used(self, url: Url, **kwargs):
        super(Proxy, self).used(**kwargs)
        self._domains[url.domain].used(**kwargs)

    def __eq__(self, other)->bool:
        return other is not None and isinstance(other, Proxy) and self._domain == other._domain

    def ___repr___(self):
        return {
            **super(Proxy, self).___repr___(),
            **{
                "domain": self._domain.___repr___(),
                "domains": {
                    key.domain: value.___repr___() for key, value in self._domains.items()
                }
            }}
