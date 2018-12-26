"""Creates a structure to hold parsed robots txts."""
from ..expirables import ExpirableRobotFileParser, Domain, Url, DomainsDict
from ..utils import Printable
from typing import Dict


class Robots(Printable):
    """Creates a structure to hold parsed robots txts."""

    def __init__(self, **kwargs):
        """Creates a structure to hold parsed robots txts.
            follow_robot_txt:bool, whetever to follow robots txt in the first place.
            useragent:str, useragent to test robots with.
            default_url_timeout:float, url default timeout if no other one is given by robots.
            robots_timeout:float, timeout after which robots file is re-downloaded.
            follow_robot_txt_black_list:List[Domain], list of domains to not follow robots txts. Overrides follow_robot_txt value, if provided.
            follow_robot_txt_white_list:List[Domain], list of domains to follow robots txts. Overrides follow_robot_txt value, if provided.
        """
        assert isinstance(kwargs["follow_robot_txt"], bool)
        assert isinstance(kwargs["useragent"], str)
        assert isinstance(kwargs["default_url_timeout"], (float, int))
        assert isinstance(kwargs["robots_timeout"], (float, int))
        self._domains = DomainsDict(ExpirableRobotFileParser)
        self._useragent = kwargs["useragent"]
        self._default_url_timeout = kwargs["default_url_timeout"]
        self._robots_timeout = kwargs["robots_timeout"]
        self._follow_robot_txt = kwargs["follow_robot_txt"]
        self._follow_robot_txt_black_list = kwargs.get(
            "follow_robot_txt_black_list",
            []
        )
        self._follow_robot_txt_white_list = kwargs.get(
            "follow_robot_txt_white_list",
            []
        )

    def follow(self, domain: Domain)->bool:
        """Determine whetever to follow or not a given domain.
            domain:Domain, domain to check for.
        """
        return domain in self._follow_robot_txt_white_list or domain not in self._follow_robot_txt_black_list and self._follow_robot_txt

    def _handle_creation(self, domain: Domain):
        """Creates ExpirableRobotFileParser if not already present"""
        if domain not in self._domains:
            self._domains[domain] = ExpirableRobotFileParser(
                domain,
                self._useragent,
                self.follow(domain),
                self._default_url_timeout,
                use_timeout=self._robots_timeout
            )

    def can_download(self, url: Url)->bool:
        """Return a boolean representing if url can be downloaded.
            url:Url, url to check for.
        """
        self._handle_creation(url.domain)
        return self._domains[url.domain].can_download(url.url)

    def get_timeout(self, domain: Domain)->float:
        """Return a float representing what has to be waited for a given domain.
            domain:Domain, domain to check for.
        """
        self._handle_creation(domain)
        return self._domains[domain].timeout

    def ___repr___(self)->Dict:
        """Return a dictionary representation of object."""
        return {
            "domains": self._domains.___repr___(),
            "useragent": self._useragent,
            "default_url_timeout": self._default_url_timeout,
            "robots_timeout": self._robots_timeout,
            "follow_robot_txt": self._follow_robot_txt,
            "follow_robot_txt_black_list": self._follow_robot_txt_black_list,
            "follow_robot_txt_white_list": self._follow_robot_txt_white_list
        }
