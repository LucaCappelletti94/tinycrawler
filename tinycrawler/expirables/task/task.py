from ..sporadic_expirable import SporadicExpirable
from ...exceptions import IllegalArgumentError


class Task(SporadicExpirable):
    UNASSIGNED = "UNASSIGNED"
    ASSIGNED = "ASSIGNED"
    FAILURE = "FAILURE"
    SUCCESS = "SUCCESS"

    TASK_NAMES = {
        UNASSIGNED: UNASSIGNED,
        ASSIGNED: ASSIGNED,
        FAILURE: FAILURE,
        SUCCESS: SUCCESS
    }

    def __init__(self, task_id: int, **kwargs):
        """Create an unique task.
            task_id:int, unique identifier of current task.
        """
        super(Task, self).__init__(**kwargs)
        self._status = Task.UNASSIGNED
        self._task_id = task_id

    def use(self, **kwargs):
        super(Task, self).use(**kwargs)
        self._status = Task.ASSIGNED

    def used(self, **kwargs):
        super(Task, self).used(success=False)
        self._status = Task.UNASSIGNED

    def is_available(self, **kwargs):
        return super(Task, self).is_available(**kwargs)

    @property
    def status(self):
        return self._status

    @property
    def task_id(self):
        return self._task_id

    @status.setter
    def status(self, status: int):
        if status not in Task.TASK_NAMES:
            raise IllegalArgumentError(
                "Given status {status} is invalid.".format(status=status))
        self._status = status

    def __hash__(self):
        return self.task_id

    def __eq__(self, other):
        return other is not None and other.__hash__() == self.__hash__()

    def ___repr___(self):
        return {
            **super(Task, self).___repr___(),
            **{
                "task_id": self.task_id,
                "task_status": Task.TASK_NAMES[self.status]
            }}
