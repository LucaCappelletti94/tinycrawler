from ..collections import ExpirablesQueue
from ..web import Domain, DomainsDict
from .task import Task
from typing import Type
from ...exceptions import IllegalArgumentError
from queue import Empty
from ...utils import Printable


class TasksQueue(Printable):
    def __init__(self, task_type: Type):
        if not issubclass(task_type, Task):
            raise IllegalArgumentError(
                "Given type {type} is not a subclass of TasksQueue".format(
                    type=task_type.__name__
                ))
        self._task_type = task_type
        self._tasks = ExpirablesQueue(task_type)
        self._client_specific_tasks = DomainsDict(ExpirablesQueue)

    def pop(self, ip: Domain, **kwargs):
        if ip in self._client_specific_tasks:
            try:
                return self._client_specific_tasks[ip].pop(**kwargs)
            except Empty:
                pass
        return self._tasks.pop(**kwargs)

    def add(self, task, ip: Domain = None, **kwargs):
        if ip is None:
            self._tasks.add(task, **kwargs)
        else:
            if ip not in self._client_specific_tasks:
                self._client_specific_tasks[ip] = ExpirablesQueue(
                    self._task_type
                )
            self._client_specific_tasks[ip].add(task, **kwargs)

    def ___repr___(self)->dict:
        return {
            "type": self._task_type.__name__,
            "tasks": self._tasks.___repr___(),
            "client_specific_tasks": self._client_specific_tasks.___repr___()
        }
