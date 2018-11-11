"""Handle UrlJob."""
from .job import Job
from ..statistics import Statistics
from ..log import Log
from ..utils import get_domain
from urllib.robotparser import RobotFileParser


class RobotsJob(dict):
    """Handle RobotsJob."""

    def __init__(self, logger: Log, statistics: Statistics):
        self._statistics, self._logger = statistics, logger

    def can_fetch(self, url: str)->bool:
        """Return a bool representing if given url can be parsed.
            url:str, the url to check for.
        """
        domain = get_domain(url)
        if domain not in self:
            self._retrieve_robots_txt(domain)
        return self[domain].can_fetch("*", url)

    def _retrieve_robots_txt(self, domain: str):
        """Dowload robots.txt from given domain and parses it.
            domain:str, the domain from which to download the robots.txt
        """
        r = RobotFileParser("{domain}/robots.txt".format(domain=domain))
        r.read()
        self[domain] = r
