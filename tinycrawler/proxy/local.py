from typing import Callable
from ..robots import Robots
from .proxy import Proxy


class Local(Proxy):
    def __init__(self, domains_timeout: float, custom_domains_timeout: Callable[[str], float], follow_robots_txt: bool, robots: Robots):
        super().__init__(None, 0, domains_timeout,
                         custom_domains_timeout, follow_robots_txt, robots)

    def is_local(self):
        return True
