from multiprocessing.managers import BaseManager
import multiprocessing
from ..log import Log
from ..urls import Urls
from ..statistics import Statistics
from ..robots import Robots
from typing import Callable
from ..proxy import Local

backup_autoproxy = multiprocessing.managers.AutoProxy


def redefined_autoproxy(token, serializer, manager=None, authkey=None,
                        exposed=None, incref=True, manager_owned=True):
    return backup_autoproxy(token, serializer, manager, authkey,
                            exposed, incref)


multiprocessing.managers.AutoProxy = redefined_autoproxy


class TinyCrawlerManager(BaseManager):
    def Statistics(self)->Statistics:
        raise NotImplementedError(
            "Method Statistics should be called by registration.")

    def Log(self, log_filename: str)->Log:
        raise NotImplementedError(
            "Method Log should be called by registration.")

    def Urls(self, statistics: Statistics, bloom_filters_capacity: int)->Urls:
        raise NotImplementedError(
            "Method Urls should be called by registration.")

    def Robots(self, robots_timeout: float)->Robots:
        raise NotImplementedError(
            "Method Robots should be called by registration.")

    def Local(self, domains_timeout: float, custom_domains_timeout: Callable[[str], float], follow_robots_txt: bool, robots: Robots)->Local:
        raise NotImplementedError(
            "Method Local should be called by registration.")


TinyCrawlerManager.register('Urls', Urls)
TinyCrawlerManager.register('Statistics', Statistics)
TinyCrawlerManager.register('Log', Log)
TinyCrawlerManager.register('Robots', Robots)
TinyCrawlerManager.register('Local', Local)
