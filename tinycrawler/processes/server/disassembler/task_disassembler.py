"""Define a process to disassemble tasks."""
from ...queue_process import QueueProcess
from ....expirables import TasksQueue, Task
from typing import Tuple


class TaskDisassembler(QueueProcess):
    """Define a process to disassemble tasks."""

    def __init__(self, tasks: TasksQueue, **kwargs):
        """Define a process to disassemble tasks.
            stop: Event, event to signal to process that the end has been reached.
            logger: Logger, logger where to log the process exceptions.
            max_waiting_timeout: float, maximum amount of time that the process has to wait doing nothing before quitting.
            tasks: TasksQueue, completed tasks to disassemble.
        """
        super(TaskDisassembler, self).__init__(**kwargs)
        self._tasks = tasks

    def _sink(self, *args):
        pass

    def _source(self)->Tuple[Task]:
        return (self._tasks.pop(),)
