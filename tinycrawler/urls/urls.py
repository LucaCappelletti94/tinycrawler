from pybloom_live import BloomFilter
from ..statistics import Statistics
from multiprocessing import Lock, Queue
from typing import List, Set, Tuple
from queue import Empty
from ..utils import get_domain


class Urls:

    def __init__(self, statistics: Statistics, bloom_filters_capacity: int):
        self._bloom = BloomFilter(
            capacity=bloom_filters_capacity
        )
        self._put_lock = Lock()
        self._domains = {}

    def get(self, domains: Set[str])->Tuple[str, bool]:
        for domain in set(self._domains.keys()) - set(domains):
            try:
                return self._domains[domain].get_nowait(), True
            except Empty:
                pass
        for queue in self._domains.values():
            try:
                return queue.get_nowait(), False
            except Empty:
                pass
        return None, False

    def put(self, urls: List[str]):
        n = 0
        self._put_lock.acquire()
        for url in urls:
            if url not in self._bloom:
                self._bloom.add(url)
                domain = get_domain(url)
                if domain not in self._domains:
                    self._domains[domain] = Queue()
                self._domains[domain].put(url)
                n += 1
        self._put_lock.release()
        return n
