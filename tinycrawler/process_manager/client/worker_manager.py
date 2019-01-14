"""Create a new manager of generic task worker processes."""
from ..queue_process_manager import QueueProcessManager
from ...expirables import TasksQueue, ClientData, TasksSink
from typing import Dict


class WorkerManager(QueueProcessManager):
    """Create a new manager of generic task worker processes."""

    def __init__(self, client_data: ClientData, tasks: TasksQueue, completed_tasks: TasksSink, **kwargs):
        """Create a new manager of generic task worker processes.
            stop: Event, event to signal to process that the end has been reached.
            logger: Logger, logger where to log the process exceptions.
            max_waiting_timeout: float, maximum amount of time that the process has to wait doing nothing before quitting.
            max_processes: int, maximum number of processes of this kind that can be spawned.
            client_data: ClientData, informations about the client that is running this Worker process.
            tasks: TasksQueue, queue of tasks that the worker will run through.
            completed_tasks: TasksSink, queue of tasks where the worker will put completed tasks.
        """
        super(WorkerManager, self).__init__(**kwargs)
        self._client_data = client_data
        self._tasks = tasks
        self._completed_tasks = completed_tasks

    @property
    def _kwargs(self)->Dict:
        """Spawn a new generic task worker process."""
        return {
            **super(WorkerManager, self)._kwargs,
            "client_data": self._client_data,
            "tasks": self._tasks,
            "completed_tasks": self._completed_tasks
        }

    def can_spawn(self)->bool:
        """Return a boolean representing if a new worker process can be spawned."""
