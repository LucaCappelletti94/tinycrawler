from ...collections import Sporadic
from collections import namedtuple
from .domain import Domain
from urllib.robotparser import RobotFileParser

RequestRate = namedtuple("RequestRate", "requests seconds")


class ExpirableRobotFileParser(Sporadic):
    def __init__(self, domain: Domain, useragent: str, follow_robots: bool, default_timeout: float, **kwargs):
        super(ExpirableRobotFileParser, self).__init__(**kwargs)
        self._domain = domain
        self._useragent = useragent
        self._follow_robots = follow_robots
        self._default_timeout = default_timeout
        self._robots = RobotFileParser(self.robots_txt_address)

    @property
    def robots_txt_address(self):
        return "http://{domain}/robots.txt".format(domain=self._domain.domain)

    @property
    def _crawl_delay_(self)->float:
        return self._robots.crawl_delay(self._useragent) or 0 if self._follow_robots else 0

    @property
    def _request_rate_(self)->RequestRate:
        return self._robots.request_rate(self._useragent) or RequestRate(1, 0) if self._follow_robots else RequestRate(1, 0)

    @property
    def _request_rate_delay_(self)->float:
        rate = self._request_rate_
        return rate.seconds / rate.requests

    @property
    def timeout(self):
        """Return a float representing what has to be waited for current domain."""
        self._update()
        return max(self._crawl_delay_, self._request_rate_delay_, self._default_timeout)

    def can_download(self, url: str)->bool:
        """Return a boolean representing if url can be downloaded.
            url:Url, url to check for.
        """
        if not self._follow_robots:
            return True
        self._update()
        return self._robots.can_fetch(
            self._useragent,
            url
        )

    def _update(self):
        if self._follow_robots and super(ExpirableRobotFileParser, self).is_available():
            self._robots.read()
            super(ExpirableRobotFileParser, self).use()

    def ___repr___(self):
        rate = self._request_rate_
        return {
            **super(ExpirableRobotFileParser, self).___repr___(),
            **{
                "domain": self._domain.___repr___(),
                "useragent": self._useragent,
                "crawl_delay": self._crawl_delay_,
                "follow_robots": self._follow_robots,
                "request_rate": {
                    "seconds": rate.seconds,
                    "requests": rate.requests
                },
                "request_rate_delay": self._request_rate_delay_,
                "timeout": self.timeout
            }}
