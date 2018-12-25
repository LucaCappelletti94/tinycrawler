from ..sporadic_sequential_expirable import SporadicSequentialExpirable
from urllib.parse import urlparse
from validators import url as is_url_valid
from IPy import IP


class Domain(SporadicSequentialExpirable):

    def __init__(self, url: str, **kwargs):
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
    def is_ip_valid(url: str):
        try:
            return IP(url)
        except ValueError:
            return False

    @property
    def domain(self):
        return self._domain

    def __hash__(self):
        return hash(self.domain)

    def __eq__(self, other):
        return other is not None and isinstance(other, Domain) and self.domain == other.domain

    def ___repr___(self):
        return {
            **super(Domain, self).___repr___(),
            **{
                "domain": self.domain
            }}
