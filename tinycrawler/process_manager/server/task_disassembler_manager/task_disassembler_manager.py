"""Create a new manager of generic task worker processes."""
from ...queue_process_manager import QueueProcessManager
from ....expirables import TasksQueue


class TaskDisassemblerManager(QueueProcessManager):
    """Create a new manager of generic task worker processes."""

    def __init__(self, tasks: TasksQueue, process, **kwargs):
        """Create a new manager of task assembling processes.
            stop: Event, event to signal to process that the end has been reached.
            logger: Logger, logger where to log the process exceptions.
            max_waiting_timeout: float, maximum amount of time that the process has to wait doing nothing before quitting.
            max_processes: int, maximum number of processes of this kind that can be spawned.
            tasks: TasksQueue, queue where to add created tasks.
            process, class of the process to spawn.
        """
        super(TaskDisassemblerManager, self).__init__(**kwargs)
        self._tasks = tasks
        self._process = process

    def spawn(self):
        """Spawn a new task assembler process."""
        return self._process(
            **super(TaskDisassemblerManager, self)._kwargs,
            tasks=self._tasks
        )
