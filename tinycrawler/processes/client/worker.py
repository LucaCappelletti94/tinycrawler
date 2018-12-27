"""Create a generic task worker process."""
from ..queue_process import QueueProcess
from ...expirables import TasksQueue, Task, ClientData, ExpirablesQueue
from typing import Tuple


class Worker(QueueProcess):
    """Create a generic task worker process."""

    def __init__(self, client_data: ClientData, tasks: TasksQueue, completed_tasks: ExpirablesQueue, **kwargs):
        """Create a generic task worker process."""
        super(Worker, self).__init__(**kwargs)
        assert isinstance(client_data, ClientData)
        self._tasks = tasks
        self._completed_tasks = completed_tasks
        self._client_data = client_data

    def _sink(self, *args):
        self._completed_tasks.add(args[0])

    def _job(self, *args)->Tuple[Task]:
        success, status = False, Task.FAILURE
        (task,) = args
        task.use()
        if self._work(task):
            success, status = True, Task.SUCCESS
        task.used(success=success)
        task.status = status
        return (task,)

    def _work(self, task: Task)->bool:
        """Handle the logical execution of the job."""
        raise NotImplementedError(
            "Method `_work` has to implement by subclasses of QueueProcess"
        )

    def _source(self)->Tuple[Task]:
        return (self._tasks.pop(self._client_data.ip),)
