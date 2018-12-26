from ...queue_process import QueueProcess
from ....expirables import TasksQueue, Domain, Task
from typing import Dict


class TaskAssembler(QueueProcess):
    def __init__(self, tasks: TasksQueue, task_kwargs: Dict, **kwargs):
        super(TaskAssembler, self).__init__(**kwargs)
        self._tasks = tasks
        self._task_kwargs = task_kwargs

    def _sink(self, task: Task, ip: Domain = None):
        self._tasks.add(task, ip)
