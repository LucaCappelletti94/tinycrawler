"""Create object representing an Url."""
from ..sporadic_sequential_expirable import SporadicSequentialExpirable
from ...collections import Sporadic
from .domain import Domain


class Url(SporadicSequentialExpirable):
    """Create object representing an Url."""

    def __init__(self, url: str, **kwargs):
        """Create object representing an Url.
            maximum_consecutive_errors:int, maximum number of consecutive errors before object expires.
            maximum_error_rate:float, maximum threshold of error/attempts before the object expires.
        """
        assert "maximum_usages" not in kwargs
        assert "use_timeout" not in kwargs
        assert "used_timeout" not in kwargs
        super(Url, self).__init__(maximum_usages=1, use_timeout=0, **kwargs)
        self._domain = Domain(url)
        self._url = url

    @property
    def domain(self)->Domain:
        """Return url's Domain object."""
        return self._domain

    @property
    def url(self)->str:
        """Return url string."""
        return self._url

    @property
    def timeout(self)->float:
        """Return timeout after which url is available on usage."""
        return self._use_timeout

    @timeout.setter
    def timeout(self, timeout: float):
        """Set timeout after which url is available on usage.
            timeout:float, timeout value.
        """
        assert isinstance(timeout, (float, int))
        if self._used_timeout != timeout:
            if not Sporadic.is_available(self) and self._used_timeout < timeout:
                self._set_available_time(timeout)
            self._used_timeout = timeout

    def __hash__(self):
        """Define hash function for Domain objects."""
        return hash(self._url)

    def __eq__(self, other):
        """Define equal rule for Domain objects."""
        return other is not None and isinstance(other, Url) and self.__hash__() == other.__hash__()

    def ___repr___(self):
        """Return a dictionary representation of object."""
        return {
            **super(Url, self).___repr___(),
            **{
                "domain": self.domain.___repr___(),
                "url": self.url
            }}
