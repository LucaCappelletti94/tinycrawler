"""Create an unique task"""
from ..sporadic_sequential_expirable import SporadicSequentialExpirable
from ..client_data import ClientData
from typing import Dict


class Task(SporadicSequentialExpirable):
    """Create an unique task"""
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
        self._client = None

    def use(self, **kwargs):
        """Update use task status."""
        super(Task, self).use(**kwargs)
        self._status = Task.ASSIGNED

    def used(self, **kwargs):
        """Update used task status."""
        super(Task, self).used(**kwargs)
        self._status = Task.UNASSIGNED

    @property
    def status(self)->str:
        """Return task's status."""
        return self._status

    @property
    def failed(self)->bool:
        """Return boolean representing if task has failed."""
        return self.status == self.FAILURE

    @property
    def succeded(self)->bool:
        """Return boolean representing if task has succeded."""
        return self.status == self.SUCCESS

    @property
    def new(self)->bool:
        """Return boolean representing if task still has to receive its id."""
        return self._task_id is None

    @property
    def client(self)->ClientData:
        """Return boolean representing if task still has to receive its id."""
        assert self._client is not None
        return self._client

    @property
    def task_id(self)->int:
        """Return task's id."""
        assert not self.new
        return self._task_id

    @task_id.setter
    def task_id(self, task_id: int):
        """Set task's id.
            task_id:int, task new id.
        """
        assert self.new
        self._task_id = task_id

    @client.setter
    def client(self, client: ClientData):
        """Set task's id.
            client:ClientData, task client executor.
        """
        assert self._client is None
        self._client = client

    @status.setter
    def status(self, status: str):
        """Set task's status.
            task_status:int, task new status.
        """
        assert status in Task.TASK_NAMES
        self._status = status

    def __hash__(self):
        """Define hash function for Domain objects."""
        return self.task_id

    def __eq__(self, other):
        """Define equal rule for Domain objects."""
        return other is not None and isinstance(other, Task) and other.__hash__() == self.__hash__()

    def ___repr___(self)->Dict:
        """Return a dictionary representation of object."""
        return {
            **super(Task, self).___repr___(),
            **{
                "task_id": self.task_id,
                "task_status": Task.TASK_NAMES[self.status]
            }}
