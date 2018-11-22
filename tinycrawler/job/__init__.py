"""Import classes for queueing in multiprocessing."""
from .filejob import FileJob
from .proxyjob import ProxyJob
from .urljob import UrlJob
from .job import Job
from .robotsjob import RobotsJob

__all__ = ['FileJob', 'UrlJob', 'ProxyJob', 'RobotsJob', 'Job']
