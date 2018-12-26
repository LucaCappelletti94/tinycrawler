"""Create a queue of tasks of given type."""
from ..collections import ExpirablesQueue
from ..web import Domain, DomainsDict
from .task import Task
from typing import Type, Dict
from queue import Empty
from ...utils import Printable
from multiprocessing import Lock


class TasksQueue(Printable):
    """Create a queue of tasks of given type."""

    def __init__(self, task_type: Type):
        """Create a queue of tasks of given type.
            task_type: Type, type of tasks
        """
        assert issubclass(task_type, Task)
        self._task_type = task_type
        self._tasks = ExpirablesQueue(task_type)
        self._client_specific_tasks = DomainsDict(ExpirablesQueue)
        self._add_lock = Lock()
        self._counter = 0

    def pop(self, ip: Domain = None, **kwargs)->Task:
        """Return first available task at given ip, if provided.
            ip: Domain, optional, specifies the ip of the workers for the task.
        """
        if ip is not None and ip in self._client_specific_tasks:
            try:
                return self._client_specific_tasks[ip].pop(**kwargs)
            except Empty:
                pass
        return self._tasks.pop(**kwargs)

    def add(self, task: Task, ip: Domain = None, **kwargs):
        """Add given task to its queue.
            task: Task, task to be added
            ip: Domain, optional, specifies the ip of the workers for the task.
        """
        if task.new:
            with self._add_lock:
                task.task_id = self._counter
                self._counter += 1
        if ip is None:
            self._tasks.add(task, **kwargs)
        else:
            if ip not in self._client_specific_tasks:
                self._client_specific_tasks[ip] = ExpirablesQueue(
                    self._task_type
                )
            self._client_specific_tasks[ip].add(task, **kwargs)

    def ___repr___(self)->Dict:
        """Return a dictionary representation of object."""
        return {
            "type": self._task_type.__name__,
            "tasks": self._tasks.___repr___(),
            "client_specific_tasks": self._client_specific_tasks.___repr___()
        }
