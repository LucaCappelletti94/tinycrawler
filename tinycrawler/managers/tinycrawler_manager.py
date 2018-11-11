from multiprocessing.managers import BaseManager
import multiprocessing
from ..statistics import Statistics as OldStatistics
from ..log import Log as OldLog
from ..job import UrlJob as OldUrlJob, FileJob as OldFileJob, ProxyJob as OldProxyJob, RobotsJob as OldRobotsJob

backup_autoproxy = multiprocessing.managers.AutoProxy


def redefined_autoproxy(token, serializer, manager=None, authkey=None,
                        exposed=None, incref=True, manager_owned=True):
    return backup_autoproxy(token, serializer, manager, authkey,
                            exposed, incref)


multiprocessing.managers.AutoProxy = redefined_autoproxy


class TinyCrawlerManager(BaseManager):

    Log = OldLog.__init__
    Statistics = OldStatistics.__init__
    UrlJob = OldUrlJob.__init__
    FileJob = OldFileJob.__init__
    ProxyJob = OldProxyJob.__init__
    RobotsJob = OldRobotsJob.__init__


TinyCrawlerManager.register('Statistics', OldStatistics)
TinyCrawlerManager.register('Log', OldLog)
TinyCrawlerManager.register('UrlJob', OldUrlJob)
TinyCrawlerManager.register('FileJob', OldFileJob)
TinyCrawlerManager.register('ProxyJob', OldProxyJob)
TinyCrawlerManager.register('RobotsJob', OldRobotsJob)
