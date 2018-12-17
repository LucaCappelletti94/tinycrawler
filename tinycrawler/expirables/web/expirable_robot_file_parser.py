from ...collections import Sporadic
from .domain import Domain
from multiprocessing import Lock
from urllib.robotparser import RobotFileParser, RequestRate


class ExpirableRobotFileParser(Sporadic):
    def __init__(self, domain: Domain, useragent: str, **kwargs):
        super(ExpirableRobotFileParser, self).__init__(**kwargs)
        self._domain = domain
        self._useragent = useragent
        self._update_lock = Lock()
        self._robots = RobotFileParser(self.robots_txt_address)

    @property
    def robots_txt_address(self):
        return "http://{domain}/robots.txt".format(domain=self._domain.domain)

    @property
    def _crawl_delay_(self)->float:
        return self._robots.crawl_delay(self._useragent) or 0

    @property
    def _request_rate_(self)->RequestRate:
        return self._robots.request_rate(self._useragent) or RequestRate(1, 0)

    @property
    def _request_rate_delay_(self)->float:
        rate = self._request_rate_
        return rate.seconds / rate.requests

    @property
    def timeout(self):
        self._update()
        return max(self._crawl_delay_, self._request_rate_delay_)

    def can_fetch(self, url: str)->bool:
        self._update()
        return self._robots.can_fetch(
            self._useragent,
            url
        )

    def _update(self):
        if super(ExpirableRobotFileParser, self).is_available():
            self._update_lock.acquire()
            if super(ExpirableRobotFileParser, self).is_available():
                self._robots.read()
                super(ExpirableRobotFileParser, self).use()
            self._update_lock.release()

    def ___repr___(self):
        return {
            **super(ExpirableRobotFileParser, self).___repr___(),
            **{
                "domain": self._domain.___repr___(),
                "useragent": self._useragent,
                "crawl_delay": self._crawl_delay_,
                "request_rate": self._request_rate_,
                "request_rate_delay": self._request_rate_delay_,
                "timeout": self.timeout
            }}
