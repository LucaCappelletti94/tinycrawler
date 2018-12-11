"""Handle UrlJob."""
from ..statistics import Statistics
from ..log import Log
from ..utils import get_domain
from urllib.robotparser import RobotFileParser
from ..eta import Eta


class Robots(dict):
    """Handle RobotsJob."""

    def __init__(self, robots_timeout: float, follow_robots_txt: bool):
        self._eta = Eta(robots_timeout)
        self._follow_robots_txt = follow_robots_txt

    def can_fetch(self, url: str)->bool:
        """Return a bool representing if given url can be parsed.
            url:str, the url to check for.
        """
        if not self._follow_robots_txt:
            return True
        domain = get_domain(url)
        self._validity_check(domain)
        return self[domain].can_fetch("*", url)

    def timeout(self, domain: str)->float:
        if not self._follow_robots_txt:
            return 0
        self._validity_check(domain)
        delay = self[domain].crawl_delay("*")
        requests_rate = self[domain].request_rate("*")
        requests_rate_delay = 0
        if delay is None:
            delay = 0
        if requests_rate is not None:
            requests_rate_delay = requests_rate.seconds / requests_rate.requests
        return max(delay, requests_rate_delay)

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
