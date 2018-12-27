"""Define a process to create tasks."""
from ...queue_process import QueueProcess
from ....expirables import TasksQueue
from typing import Dict


class TaskAssembler(QueueProcess):
    """Define a process to create tasks."""

    def __init__(self, tasks: TasksQueue, task_kwargs: Dict, **kwargs):
        """Define a process to create tasks."""
        super(TaskAssembler, self).__init__(**kwargs)
        self._tasks = tasks
        self._task_kwargs = task_kwargs

    def _sink(self, *args):
        self._tasks.add(*args)
