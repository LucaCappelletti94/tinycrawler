"""Define a process to create tasks."""
from ...queue_process import QueueProcess
from ....expirables import TasksQueue
from typing import Dict


class TaskAssembler(QueueProcess):
    """Define a process to create tasks."""

    def __init__(self, tasks: TasksQueue, task_kwargs: Dict, **kwargs):
        """Define a process to create tasks.
            stop: Event, event to signal to process that the end has been reached.
            logger: Logger, logger where to log the process exceptions.
            max_waiting_timeout: float, maximum amount of time that the process has to wait doing nothing before quitting.
            tasks: TasksQueue, queue where to add created tasks.
            task_kwargs: Dict, argument to pass to the tasks.
        """
        super(TaskAssembler, self).__init__(**kwargs)
        self._tasks = tasks
        self._task_kwargs = task_kwargs

    def _sink(self, *args):
        self._tasks.add(*args)
