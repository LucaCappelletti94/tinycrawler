from ..sporadic_sequential_expirable import SporadicSequentialExpirable
from urllib.parse import urlparse
from ...exceptions import IllegalArgumentError
from validators import url as is_url_valid


class Domain(SporadicSequentialExpirable):

    def __init__(self, url: str, **kwargs):
        super(Domain, self).__init__(**kwargs)
        if not is_url_valid(url):
            raise IllegalArgumentError(
                "Given url {url} is not a valid url.".format(url=url))
        self._domain = self._get_domain(url)

    def _get_domain(self, url: str)->str:
        """Return domain from given url.
            url:str, the url from which extract the domain.
        """
        return '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))

    @property
    def domain(self):
        return self._domain

    def __hash__(self):
        return hash(self.domain)

    def __eq__(self, other):
        return other is not None and isinstance(other, Domain) and self.__hash__() == other.__hash__()

    def ___repr___(self):
        return {
            **super(Domain, self).___repr___(),
            **{
                "domain": self.domain
            }}
