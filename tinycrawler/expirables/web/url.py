from ..sporadic_sequential_expirable import SporadicSequentialExpirable
from ...collections import Sporadic
from .domain import Domain


class Url(SporadicSequentialExpirable):

    def __init__(self, url: str, **kwargs):
        """Create object representing an Url.
            use_timeout:float, unavailability timeout after use.
            used_timeout:float, unavailability timeout after used.
            maximum_usages:int, maximum parallel usages.
            maximum_consecutive_errors:int, maximum number of consecutive errors before object expires.
            maximum_error_rate:float, maximum threshold of error/attempts before the object expires.
        """
        super(Url, self).__init__(**kwargs)
        self._domain = Domain(url)
        self._url = url

    @property
    def domain(self):
        return self._domain

    @property
    def url(self):
        return self._url

    @property
    def timeout(self)->float:
        return self._use_timeout

    @timeout.setter
    def timeout(self, timeout: float):
        if self._use_timeout != timeout:
            self._use_timeout = timeout
            if not Sporadic.is_available(self):
                self._set_available_time(self._use_timeout)

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
