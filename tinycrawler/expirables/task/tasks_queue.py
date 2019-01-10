"""Create a queue of tasks of given type."""
from ..collections import ExpirablesQueue
from ..web import Domain
from .task import Task
from typing import Dict
from queue import Empty
from ...utils import Printable
from multiprocessing import Lock


class TasksQueue(Printable):
    """Create a queue of tasks of given type."""

    def __init__(self):
        """Create a queue of tasks."""
        self._tasks = {}
        self._client_domains = {}
        self._add_lock = Lock()
        self._counter = 0

    def _pop(self, ip: Domain, **kwargs)->Task:
        """Return first available task at given ip, if provided.
            ip: Domain, optional, specifies the ip of the workers for the task.
        """
        if ip is not None and ip in self._client_domains:
            try:
                return self._client_domains[ip].pop(**kwargs)
            except Empty:
                pass
        return self._tasks.pop(**kwargs)

    def pop(self, ip: Domain = None, **kwargs)->Task:
        """Return first available task at given ip, if provided.
            ip: Domain, optional, specifies the ip of the workers for the task.
        """
        assert isinstance(ip, (Domain, None))
        task = self._pop(ip, **kwargs)
        task.use()
        self.add(task, ip)
        return task

    def delete(self, task: Task)->bool:
        """Delete given task from queue and return boolean representing if task has been deleted.
            task: Task, task to be deleted.
        """
        for client_domain in self._client_domains:
            if task in self._client_domains[client_domain]:
                del self._client_domains[client_domain][task]
                return True
        if task in self._tasks:
            del self._tasks[task]
            return True
        return False

    def add(self, task: Task, ip: Domain = None, **kwargs):
        """Add given task to its queue.
            task: Task, task to be added
            ip: Domain, optional, specifies the ip of the workers for the task.
        """
        assert isinstance(task, Task)
        assert isinstance(ip, (Domain, None))
        assert not task.expired
        assert not ip.expired
        if task.new:
            with self._add_lock:
                task.task_id = self._counter
                self._counter += 1
        if ip is None:
            self._tasks[task] = task
        else:
            if ip not in self._client_domains:
                self._client_domains[ip] = ExpirablesQueue()
            self._client_domains[ip].add(task, **kwargs)

    def ___repr___(self)->Dict:
        """Return a dictionary representation of object."""
        return {
            "tasks": self._tasks,
            "client_specific_tasks": self._client_domains
        }
