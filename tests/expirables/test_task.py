from tinycrawler.expirables.task.task import Task
from ..commons import mock_repr
import pytest


def setup():
    return Task()


def test_task_eq():
    t1 = setup()
    t2 = setup()
    t1.task_id = t2.task_id = 3

    assert t1 == t2


def test_task():
    task = setup()
    with pytest.raises(AssertionError):
        task.task_id

    task.task_id = 0
    with pytest.raises(AssertionError):
        task.task_id = 0

    task.use()
    task.used(success=True)
    assert task.status == Task.UNASSIGNED
    task.status = Task.SUCCESS
    with pytest.raises(AssertionError):
        task.status = "Lo kebabbo non devi manducare."


def test_task_repr():
    task = setup()
    task.task_id = 0
    mock_repr(task)
