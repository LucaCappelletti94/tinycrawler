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

    def __init__(self, **kwargs):
        """Create an unique task"""
        super(Task, self).__init__(**kwargs)
        self._status = Task.UNASSIGNED
        self._task_id = None

    def use(self, **kwargs):
        super(Task, self).use(**kwargs)
        self._status = Task.ASSIGNED

    def used(self, **kwargs):
        super(Task, self).used(success=False)
        self._status = Task.UNASSIGNED

    @property
    def status(self)->str:
        return self._status

    @property
    def new(self)->bool:
        return self._task_id is None

    @property
    def task_id(self)->int:
        if self.new:
            raise IllegalArgumentError(
                "Task's `task_id` is yet to be defined!")
        return self._task_id

    @task_id.setter
    def task_id(self, task_id: int):
        if not self.new:
            raise IllegalArgumentError(
                "Task's `task_id` has already been defined!")
        self._task_id = task_id

    @status.setter
    def status(self, status: str):
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
