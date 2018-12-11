from ..eta import Eta
from typing import Callable
from ..utils import get_domain
from ..robots import Robots


class DomainsEta(Eta):

    def __init__(self, timeout: float, custom_timeout: Callable[[str], float], robots: Robots):
        super().__init__(timeout, custom_timeout)
        self._robots = robots

    def __keytransform__(self, url: str):
        return get_domain(url)

    def default_timeout(self, domain: str):
        return max(self._timeout, self._robots.timeout(domain))
