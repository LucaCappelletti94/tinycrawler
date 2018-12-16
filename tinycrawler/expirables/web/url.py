from ..sporadic_sequential_expirable import SporadicSequentialExpirable
from .domain import Domain


class Url(SporadicSequentialExpirable):

    def __init__(self, url: str, **kwargs):
        super(Url, self).__init__(**kwargs)
        self._domain = Domain(url)
        self._url = url

    @property
    def domain(self):
        return self._domain

    @property
    def url(self):
        return self._url

    def __hash__(self):
        return hash(self._url)

    def __eq__(self, other):
        return other is not None and isinstance(other, Url) and self.__hash__() == other.__hash__()

    def ___repr___(self):
        return {
            **super(Url, self).___repr___(),
            **{
                "domain": self.domain.___repr___(),
                "url": self.url
            }}
