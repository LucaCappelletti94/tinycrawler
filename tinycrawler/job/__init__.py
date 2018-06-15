"""Import classes for queueing in multiprocessing."""
from .dictjob import DictJob
from .job import Job
from .proxyjob import ProxyJob

__all__ = ['Job', 'DictJob', 'ProxyJob']
