from multiprocessing.managers import BaseManager
import multiprocessing
from ..statistics import Statistics
from ..log import Log
from ..job import UrlJob, FileJob, ProxyJob, RobotsJob

backup_autoproxy = multiprocessing.managers.AutoProxy


def redefined_autoproxy(token, serializer, manager=None, authkey=None,
                        exposed=None, incref=True, manager_owned=True):
    return backup_autoproxy(token, serializer, manager, authkey,
                            exposed, incref)


multiprocessing.managers.AutoProxy = redefined_autoproxy


class TinyCrawlerManager(BaseManager):

    def Log(self, path: str):
        pass

    def Statistics(self):
        pass

    def UrlJob(self, statistics: Statistics, bloom_filters_number: int, bloom_filters_capacity: int):
        pass

    def FileJob(self, path: str, statistics: Statistics):
        pass

    def ProxyJob(self, statistics: Statistics, logger: Log):
        pass

    def RobotsJob(self, statistics: Statistics, logger: Log):
        pass


TinyCrawlerManager.register('Statistics', Statistics)
TinyCrawlerManager.register('Log', Log)
TinyCrawlerManager.register('UrlJob', UrlJob)
TinyCrawlerManager.register('FileJob', FileJob)
TinyCrawlerManager.register('ProxyJob', ProxyJob)
TinyCrawlerManager.register('RobotsJob', RobotsJob)
