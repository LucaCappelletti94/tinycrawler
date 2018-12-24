from ...queue_process import QueueProcess
from ....expirables import TasksQueue, Domain, Task


class TaskAssembler(QueueProcess):
    def __init__(self, tasks: TasksQueue, **kwargs):
        super(TaskAssembler, self).__init__(**kwargs)
        self._tasks = tasks

    def _sink(self, task: Task, ip: Domain = None):
        self._tasks.add(task, ip)
