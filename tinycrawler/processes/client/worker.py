from ..queue_process import QueueProcess
from ...expirables import TasksQueue, Task, ClientData
from typing import Tuple


class Worker(QueueProcess):
    def __init__(self, client_data: ClientData, tasks: TasksQueue, completed_tasks: TasksQueue, *args, **kwargs):
        super(Worker, self).__init__(*args, **kwargs)
        self._tasks = tasks
        self._completed_tasks = completed_tasks
        self._client_data = client_data

    def _sink(self, completed_task: Task):
        self._completed_tasks.add(completed_task)

    def _job(self, task: Task)->Tuple[Task]:
        success, status = False, Task.FAILURE
        if self._work(task):
            success, status = True, Task.SUCCESS
        task.used(success=success)
        task.status = status
        return (task,)

    def _work(self, task: Task):
        """Handle the logical execution of the job."""
        raise NotImplementedError(
            "Method `_work` has to implement by subclasses of QueueProcess"
        )

    def _source(self)->Tuple[Task]:
        return (self._tasks.pop(self._client_data.ip),)
