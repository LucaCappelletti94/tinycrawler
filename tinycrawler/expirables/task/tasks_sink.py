"""Create a queue of tasks."""
from .task import Task
from typing import Dict
from queue import Empty
from ...utils import Printable
from .tasks_queue import TasksQueue


class TasksSink(Printable):
    """Create a sink of tasks."""

    def __init__(self, source: TasksQueue):
        """Create a queue of tasks."""
        assert isinstance(source, TasksQueue)
        self._tasks = []
        self._source = source

    def pop(self)->Task:
        if self._tasks:
            return self._tasks.pop()
        raise Empty

    def add(self, task: Task):
        """Add given task to its queue.
            task: Task, task to be added
        """
        assert isinstance(task, Task)
        if self._source.delete(task):
            self._tasks.append(task)

    def ___repr___(self)->Dict:
        """Return a dictionary representation of object."""
        return {
            "tasks": [
                task.___repr___() for task in self._tasks
            ]
        }
