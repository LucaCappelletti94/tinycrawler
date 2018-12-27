"""Define a process to disassemble tasks."""
from ...queue_process import QueueProcess
from ....expirables import TasksQueue, Task
from typing import Tuple


class TaskDisassembler(QueueProcess):
    """Define a process to disassemble tasks."""

    def __init__(self, tasks: TasksQueue, **kwargs):
        """Define a process to disassemble tasks."""
        super(TaskDisassembler, self).__init__(**kwargs)
        self._tasks = tasks

    def _source(self)->Tuple[Task]:
        return self._tasks.pop(None)
