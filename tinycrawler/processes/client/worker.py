from ..queue_process import QueueProcess
from ...expirables import TasksQueue, Task


class Worker(QueueProcess):
    def __init__(self, tasks: TasksQueue, completed_tasks: TasksQueue, *args, **kwargs):
        super(Worker, self).__init__(*args, **kwargs)
        self._tasks = tasks
        self._completed_tasks = completed_tasks

    def _sink(self, completed_task: Task):
        self._completed_tasks.add(completed_task)

    def _source(self):
        return self._tasks.pop()
