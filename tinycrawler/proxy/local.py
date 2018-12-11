from typing import Callable
from ..robots import Robots
from .proxy import Proxy


class Local(Proxy):
    def __init__(self, max_failure_rate: float, domains_timeout: float, custom_domains_timeout: Callable[[str], float], robots: Robots):
        super().__init__(None, max_failure_rate, 0,
                         domains_timeout, custom_domains_timeout, robots)

    def _currently_used(self):
        return False
