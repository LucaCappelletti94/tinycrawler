"""Import classes for queueing in multiprocessing."""
from .filejob import FileJob
from .proxyjob import ProxyJob
from .urljob import UrlJob

__all__ = ['FileJob', 'UrlJob', 'ProxyJob']
