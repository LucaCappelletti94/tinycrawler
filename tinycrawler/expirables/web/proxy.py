from ..sporadic_sequential_expirable import SporadicSequentialExpirable
from .domains_dict import DomainsDict
from .domain import Domain
from ...utils import ProxyData


class Proxy(SporadicSequentialExpirable):
    def __init__(self, proxy_data: ProxyData, **kwargs):
        super(Proxy, self).__init__(**kwargs)
        self._domain = Domain(proxy_data.ip)
        self._data = proxy_data.data
        self._domains = DomainsDict(Domain)

    def is_available(self, domain: Domain)->bool:
        if not super(Proxy, self).is_available():
            return False
        if domain is not None and domain in self._domains:
            return self._domains[domain].is_available()
        return True

    @property
    def data(self)->ProxyData:
        return self._data

    @property
    def local(self)->bool:
        return self._data is None

    def use(self, domain: Domain, **kwargs):
        super(Proxy, self).use(domain=domain, **kwargs)
        if domain not in self._domains:
            self._domains[domain] = domain
        self._domains[domain].use(**kwargs)

    def used(self, domain: Domain, **kwargs):
        super(Proxy, self).used(**kwargs)
        self._domains[domain].used(**kwargs)

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
