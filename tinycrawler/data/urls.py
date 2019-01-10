"""Creates a structure to hold urls."""
from ..expirables import Url, CircularUrlQueue
from .robots import Robots
from pybloom_live import BloomFilter
from multiprocessing import Lock
from typing import Set
from ..utils import Printable


class Urls(Printable):
    """Creates a structure to hold urls."""

    def __init__(self,  **kwargs):
        """Creates a structure to hold urls.
            bloom_filter_capacity:int, the bloom filter capacity.
            follow_robot_txt:bool, whetever to follow robots txt in the first place.
            useragent:str, useragent to test robots with.
            default_url_timeout:float, url default timeout if no other one is given by robots.
            url_maximum_consecutive_errors:int, maximum number of consecutive errors before object expires.
            url_maximum_error_rate:float, maximum threshold of error/attempts before the object expires.
            robots_timeout:float, timeout after which robots file is re-downloaded.
            follow_robot_txt_black_list:List[Domain], list of domains to not follow robots txts. Overrides follow_robot_txt value, if provided.
            follow_robot_txt_white_list:List[Domain], list of domains to follow robots txts. Overrides follow_robot_txt value, if provided.
        """
        assert "bloom_filter_capacity" in kwargs
        assert "follow_robot_txt" in kwargs
        assert "useragent" in kwargs
        assert "default_url_timeout" in kwargs
        assert "url_maximum_consecutive_errors" in kwargs
        assert "url_maximum_error_rate" in kwargs
        assert "robots_timeout" in kwargs
        assert isinstance(kwargs["bloom_filter_capacity"], int)
        self._robots = Robots(**kwargs)
        self._bloom = BloomFilter(
            capacity=kwargs["bloom_filter_capacity"]
        )
        self._urls = CircularUrlQueue()
        self._add_lock = Lock()
        self._url_maximum_consecutive_errors = kwargs["url_maximum_consecutive_errors"]
        self._url_maximum_error_rate = kwargs["url_maximum_error_rate"]

    def pop(self)->Url:
        """Returns downloadable url."""
        url = self._urls.pop()
        while not self._robots.can_download(url):
            url = self._urls.pop()
        return url

    def _add(self, url: Url, no_bloom: bool):
        assert isinstance(url, Url)
        if (no_bloom or url.url not in self._bloom) and self._robots.can_download(url):
            self._bloom.add(url.url)
            url.timeout = self._robots.get_timeout(url.domain)
            self._urls.add(url)

    def add(self, urls: Set[Url]):
        """Add given url to urls data structure, checking if it was not already added using bloom filters and if can be downloaded using robots.
            urls:Set[Url], set of unique urls to be added
        """
        assert isinstance(urls, (Url, str)) or isinstance(urls, set) and all([
            isinstance(url, str) for url in urls
        ])
        with self._add_lock:
            if isinstance(urls, Url):
                self._add(urls, True)
            elif isinstance(urls, str):
                self._add(Url(
                    urls,
                    maximum_consecutive_errors=self._url_maximum_consecutive_errors,
                    maximum_error_rate=self._url_maximum_error_rate
                ), False)
            else:
                for url in urls:
                    self._add(Url(
                        url,
                        maximum_consecutive_errors=self._url_maximum_consecutive_errors,
                        maximum_error_rate=self._url_maximum_error_rate
                    ), False)

    def ___repr___(self):
        """Return a dictionary representation of object."""
        return {
            "robots": self._robots.___repr___(),
            "urls": self._urls.___repr___()
        }
