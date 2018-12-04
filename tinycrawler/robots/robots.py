"""Handle UrlJob."""
from ..statistics import Statistics
from ..log import Log
from ..utils import get_domain
from urllib.robotparser import RobotFileParser
from ..eta import Eta


class Robots(dict):
    """Handle RobotsJob."""

    def __init__(self, robots_timeout: float):
        self._eta = Eta(robots_timeout)

    def can_fetch(self, url: str)->bool:
        """Return a bool representing if given url can be parsed.
            url:str, the url to check for.
        """
        domain = get_domain(url)
        self._validity_check(domain)
        return self[domain].can_fetch("*", url)

    def timeout(self, domain: str)->float:
        self._validity_check(domain)
        delay = self[domain].crawl_delay("*")
        if delay:
            return delay
        return 0

    def _validity_check(self, domain):
        if domain not in self or self._eta.is_ripe(domain):
            self._retrieve_robots_txt(domain)

    def _retrieve_robots_txt(self, domain: str):
        """Dowload robots.txt from given domain and parses it.
            domain:str, the domain from which to download the robots.txt
        """
        r = RobotFileParser("{domain}/robots.txt".format(domain=domain))
        r.read()
        self._eta.add(domain)
        self[domain] = r
