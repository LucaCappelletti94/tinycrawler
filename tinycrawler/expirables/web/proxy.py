"""Create a sporadically, sequentially available proxy object that can expire."""
from ..sporadic_sequential_expirable import SporadicSequentialExpirable
from .domains_dict import DomainsDict
from .domain import Domain
from ...utils import ProxyData
from typing import Dict


class Proxy(SporadicSequentialExpirable):
    """Create a sporadically, sequentially available proxy object that can expire."""

    def __init__(self, proxy_data: ProxyData, **kwargs):
        """Create a sporadically, sequentially available proxy object that can expire."""
        super(Proxy, self).__init__(**kwargs)
        self._ip = Domain(proxy_data.ip)
        self._data = proxy_data.data
        self._domains = DomainsDict(Domain)

    def is_available(self, **kwargs)->bool:
        """Return boolean representing if given proxy and domain are available for use."""
        domain = kwargs["domain"]
        assert isinstance(domain, Domain) or domain is None
        if not super(Proxy, self).is_available(**kwargs):
            return False
        if domain is not None and domain in self._domains:
            return self._domains[domain].is_available(**kwargs)
        return True

    @property
    def data(self)->ProxyData:
        """Return proxy ProxyData object."""
        return self._data

    @property
    def ip(self)->Domain:
        """Return ip Domain object."""
        return self._ip

    @property
    def local(self)->bool:
        """Return a boolean represinting if this proxy represent one of the local clients."""
        return self._data is None

    def use(self, **kwargs):
        """Update use status in proxy and given domain.
            domain:Domain, domain to set use status for proxy.
        """
        domain = kwargs["domain"]
        assert isinstance(domain, Domain)
        super(Proxy, self).use(**kwargs)
        if domain not in self._domains:
            self._domains[domain] = domain
        self._domains[domain].use(**kwargs)

    def used(self, **kwargs):
        """Update used status in proxy and given domain.
            domain:Domain, domain to set used status for proxy.
        """
        domain = kwargs["domain"]
        assert isinstance(domain, Domain)
        super(Proxy, self).used(**kwargs)
        self._domains[domain].used(**kwargs)

    def __eq__(self, other: "Proxy")->bool:
        """Define equal rule for Domain objects."""
        return other is not None and isinstance(other, Proxy) and self.ip == other.ip

    def ___repr___(self)->Dict:
        """Return a dictionary representation of object."""
        return {
            **super(Proxy, self).___repr___(),
            **{
                "domain": self.ip.___repr___(),
                "domains": {
                    key.domain: value.___repr___() for key, value in self._domains.items()
                }
            }}
