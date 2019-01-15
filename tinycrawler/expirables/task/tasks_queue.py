"""Create a queue of tasks of given type."""
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
        self._estimated_size = 0
        self._client_domains = {}
        self._estimated_domains_size = {}
        self._add_lock = Lock()
        self._counter = 0

    def _get_first_available(self, source: Dict[Task, Task], **kwargs)->Task:
        for task in source.values():
            if task.is_available(**kwargs):
                return task
        raise Empty

    def _pop(self, ip: Domain, **kwargs)->Task:
        """Return first available task at given ip, if provided.
            ip: Domain, optional, specifies the ip of the workers for the task.
        """
        if ip is not None and ip in self._client_domains:
            try:
                task = self._get_first_available(
                    self._client_domains[ip], **kwargs)
                if not task.in_use():
                    self._estimated_domains_size[ip] -= 1
                return task
            except Empty:
                pass
        task = self._get_first_available(self._tasks, **kwargs)
        if not task.in_use():
            self._estimated_size -= 1
        return task

    def size(self, ip: Domain)->int:
        """Return an approximated size of the queue.
            ip: Domain, domain of the client for which to determine the size.
        """
        assert isinstance(ip, Domain)
        return self._estimated_size + self._estimated_domains_size.get(ip, 0)

    def pop(self, ip: Domain = None, **kwargs)->Task:
        """Return first available task at given ip, if provided.
            ip: Domain, optional, specifies the ip of the workers for the task.
        """
        assert ip is None or isinstance(ip, Domain)
        task = self._pop(ip, **kwargs)
        task.use()
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

    def add(self, task: Task, ip: Domain = None):
        """Add given task to its queue.
            task: Task, task to be added
            ip: Domain, optional, specifies the ip of the workers for the task.
        """
        assert isinstance(task, Task)
        assert ip is None or isinstance(ip, Domain) and not ip.expired
        assert not task.expired
        if task.new:
            with self._add_lock:
                task.task_id = self._counter
                self._counter += 1
        if ip is None:
            self._tasks[task] = task
            self._estimated_size += 1
        else:
            if ip not in self._client_domains:
                self._client_domains[ip] = {}
            self._client_domains[ip][task] = task
            self._estimated_domains_size[ip] = self._estimated_domains_size.get(
                ip, 0) + 1

    def ___repr___(self)->Dict:
        """Return a dictionary representation of object."""
        return {
            "tasks": {
                t_key.task_id: task.___repr___() for t_key, task in self._tasks.items()
            },
            "client_specific_tasks": {
                domain.domain: {
                    t_key.task_id: task.___repr___() for t_key, task in tasks.items()
                } for domain, tasks in self._client_domains.items()
            }
        }
