from ..ETA import ETA
from typing import Callable
from ..utils import get_domain
from ..robots import Robots


class DomainsETA(ETA):
    def __init__(self, timeout: float, custom_timeout: Callable[[str], float], follow_robots_txt: bool, robots: Robots):
        if custom_timeout is None:
            super().__init__(timeout, self._domains_timeout)
            self._follow_robots_txt, self._robots = follow_robots_txt, robots
        else:
            super().__init__(timeout, custom_timeout)

    def __keytransform__(self, url: str):
        return get_domain(url)

    def _domains_timeout(self, domain: str):
        if self._follow_robots_txt:
            return max(self._timeout, self._robots.timeout(domain))
        return self._timeout
