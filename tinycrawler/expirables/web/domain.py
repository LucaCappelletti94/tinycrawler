"""Create a sporadically, sequentially available domain object that can expire."""
from ..sporadic_sequential_expirable import SporadicSequentialExpirable
from urllib.parse import urlparse
from validators import url as is_url_valid
from IPy import IP
from typing import Dict


class Domain(SporadicSequentialExpirable):
    """Create a sporadically, sequentially available domain object that can expire."""

    def __init__(self, url: str, **kwargs):
        """Create a sporadically, sequentially available domain object that can expire.
            url:str, url from which to extract domain.
        """
        super(Domain, self).__init__(**kwargs)
        assert is_url_valid(url) or Domain.is_ip_valid(url)
        self._domain = self._get_domain(url)

    def _get_domain(self, url: str)->str:
        """Return domain from given url.
            url:str, the url from which extract the domain.
        """
        assert isinstance(url, str)
        if Domain.is_ip_valid(url):
            return url
        return '{uri.netloc}'.format(uri=urlparse(url))

    @staticmethod
    def is_ip_valid(ip: str)->bool:
        """Return a boolean representing if given string is a valid ip."""
        try:
            return IP(ip)
        except ValueError:
            return False

    @property
    def domain(self)->str:
        """Return domain string."""
        return self._domain

    def __hash__(self):
        """Define hash function for Domain objects."""
        return hash(self.domain)

    def __eq__(self, other)->bool:
        """Define equal rule for Domain objects."""
        return other is not None and isinstance(other, Domain) and self.domain == other.domain

    def ___repr___(self)->Dict:
        """Return a dictionary representation of object."""
        return {
            **super(Domain, self).___repr___(),
            **{
                "domain": self.domain
            }}
