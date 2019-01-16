"""Create a circular dictionary of domains keys and expirable queue of urls."""
from ..collections import ExpirablesQueue
from ...utils import Printable
from ..web import Url
from queue import Empty
from typing import Dict


class CircularUrlQueue(Printable):
    """Create a circular dictionary of domains keys and expirable queue of urls."""

    def __init__(self):
        """Create a circular dictionary of domains keys and expirable queue of urls."""
        self._counter = 0
        self._domain_list = []
        self._urls = {}

    def _get_cursor(self, start: int = None)->int:
        n = len(self._domain_list)
        if n == 0:
            raise Empty
        cursor = self._counter % n
        if cursor == start:
            raise Empty
        if not start:
            start = cursor
        key = self._domain_list[cursor]
        if key.expired or self._urls[key].empty():
            self._counter += 1
            return self._get_cursor(start)
        return cursor

    def pop(self)->Url:
        """Return first available url."""
        return self._urls[self._domain_list[self._get_cursor()]].pop()

    def add(self, url: Url):
        """Add given url to its domain queue.
            url: Url, url to be added.
        """
        assert isinstance(url, Url)
        assert not url.expired
        if url.domain not in self._domain_list:
            self._domain_list.append(url.domain)
            self._urls[url.domain] = ExpirablesQueue()
        self._urls[url.domain].add(url)

    def size(self)->int:
        return sum([
            q.size() for q in self._urls.values()
        ])

    def ___repr___(self)->Dict:
        """Return a dictionary representation of object."""
        return {
            "domains": [
                domain.___repr___() for domain in self._domain_list
            ],
            "urls": {
                domain.domain: urls.___repr___() for domain, urls in self._urls.items()
            }
        }
