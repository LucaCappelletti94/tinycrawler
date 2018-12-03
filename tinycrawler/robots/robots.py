"""Handle UrlJob."""
from ..statistics import Statistics
from ..log import Log
from ..utils import get_domain
from urllib.robotparser import RobotFileParser
from ..ETA import ETA


class Robots:
    """Handle RobotsJob."""

    def __init__(self, robots_timeout: float):
        self._ETA = ETA(robots_timeout)
        self._robotfiles = {}

    def can_fetch(self, url: str)->bool:
        """Return a bool representing if given url can be parsed.
            url:str, the url to check for.
        """
        domain = get_domain(url)
        self._validity_check(domain)
        return self._robotfiles[domain].can_fetch("*", url)

    def timeout(self, domain: str)->float:
        self._validity_check(domain)
        delay = self._robotfiles[domain].crawl_delay("*")
        requests_rate = self._robotfiles[domain].request_rate("*")
        if delay is None:
            delay = 0
        if requests_rate is not None:
            requests_rate_delay = requests_rate.seconds / requests_rate.requests
        else:
            requests_rate_delay = 0
        return max(delay, requests_rate_delay)

    def _validity_check(self, domain):
        if domain not in self._robotfiles or self._ETA.is_ripe(domain):
            self._retrieve_robots_txt(domain)

    def _retrieve_robots_txt(self, domain: str):
        """Dowload robots.txt from given domain and parses it.
            domain:str, the domain from which to download the robots.txt
        """
        r = RobotFileParser("{domain}/robots.txt".format(domain=domain))
        r.read()
        self._ETA.add(domain)
        self._robotfiles[domain] = r
