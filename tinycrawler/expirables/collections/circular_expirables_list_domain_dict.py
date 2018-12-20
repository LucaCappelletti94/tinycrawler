from .domains_dict import DomainsDict
from .expirables_queue import ExpirablesQueue
from ..web import Domain, Url
from typing import Type
from queue import Empty


class CircularExpirablesQueuesDomainDict(DomainsDict):
    def __init__(self):
        super(CircularExpirablesQueuesDomainDict,
              self).__init__(ExpirablesQueue)
        self._counter = 0
        self._keys_list = []

    def __setitem__(self, k, v):
        super(CircularExpirablesQueuesDomainDict, self).__setitem__(k, v)
        if k not in self._keys_list:
            self._keys_list.append(k)

    def _update_counter(self):
        self._counter += 1

    def _get_cursor(self, start: int=None)->int:
        n = len(self._keys_list)
        if n == 0:
            raise Empty
        cursor = self._counter % n
        if cursor == start:
            raise Empty
        if not start:
            start = cursor
        key = self._keys_list[cursor]
        if key.expired or self[key].empty:
            self._update_counter()
            return self._get_cursor(start)
        return cursor

    def pop(self)->Url:
        return self[self._keys_list[self._get_cursor()]].pop()

    def add(self, url: Url):
        if url.domain not in self:
            self[url.domain] = ExpirablesQueue(Url)
        self[url.domain].add(url)
