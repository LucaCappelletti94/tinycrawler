"""Create a circular dictionary of domains keys and expirable queue of urls."""
from .domains_dict import DomainsDict
from ..collections import ExpirablesQueue
from ...collections import TypeList
from ..web import Url, Domain
from queue import Empty


class CircularExpirablesQueuesDomainDict(DomainsDict):
    """Create a circular dictionary of domains keys and expirable queue of urls."""

    def __init__(self):
        """Create a circular dictionary of domains keys and expirable queue of urls."""
        super(CircularExpirablesQueuesDomainDict,
              self).__init__(ExpirablesQueue)
        self._counter = 0
        self._domain_list = TypeList(Domain)

    def __setitem__(self, domain: Domain, url: Url):
        """Set item and handle list of domain."""
        super(CircularExpirablesQueuesDomainDict,
              self).__setitem__(domain, url)
        if domain not in self._domain_list:
            self._domain_list.append(domain)

    def _update_counter(self):
        self._counter += 1

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
        if key.expired or self[key].empty():
            self._update_counter()
            return self._get_cursor(start)
        return cursor

    def pop(self)->Url:
        """Return first available url."""
        return self[self._domain_list[self._get_cursor()]].pop()

    def add(self, url: Url):
        """Add given url to its domain queue.
            url: Url, url to be added.
        """
        if url.domain not in self:
            self[url.domain] = ExpirablesQueue(Url)
        self[url.domain].add(url)
