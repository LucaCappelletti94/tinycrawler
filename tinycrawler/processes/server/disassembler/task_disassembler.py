from ...queue_process import QueueProcess
from ....expirables import TasksQueue, Task
from ....exceptions import Sleep
from queue import Empty
from typing import Tuple


class TaskDisassembler(QueueProcess):
    def __init__(self, tasks: TasksQueue, **kwargs):
        super(TaskDisassembler, self).__init__(**kwargs)
        self._tasks = tasks

    def _source(self)->Tuple[Task]:
        try:
            return self._tasks.pop(None)
        except Empty:
            raise Sleep
