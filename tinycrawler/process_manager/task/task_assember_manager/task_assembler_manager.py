"""Create a new manager of generic task worker processes."""
from ...queue_process_manager import QueueProcessManager
from ....expirables import TasksQueue
from typing import Dict


class TaskAssemblerManager(QueueProcessManager):
    """Create a new manager of generic task worker processes."""

    def __init__(self, tasks: TasksQueue, task_kwargs: Dict, **kwargs):
        """Create a new manager of task assembling processes.
            stop: Event, event to signal to process that the end has been reached.
            logger: Logger, logger where to log the process exceptions.
            max_waiting_timeout: float, maximum amount of time that the process has to wait doing nothing before quitting.
            tasks: TasksQueue, queue where to add created tasks.
            task_kwargs: Dict, argument to pass to the tasks.
        """
        super(TaskAssemblerManager, self).__init__(**kwargs)
        self._tasks = tasks
        self._task_kwargs = task_kwargs
