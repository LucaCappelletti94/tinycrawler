from tinycrawler.expirables.task.task import Task
from ..commons import mock_repr, build_repr


def setup():
    return Task()


def test_task_eq():
    t1 = setup()
    t2 = setup()
    t1.task_id = t2.task_id = 3

    assert t1 == t2


def test_task():
    task = setup()
    try:
        task.task_id
        assert False
    except AssertionError:
        pass
    task.task_id = 0
    try:
        task.task_id = 0
        assert False
    except AssertionError:
        pass
    task.use()
    task.used()
    assert task.status == Task.UNASSIGNED
    task.status = Task.SUCCESS
    try:
        task.status = "Lo kebabbo non devi manducare."
        assert False
    except AssertionError:
        pass


def test_task_repr():
    task = setup()
    task.task_id = 0
    mock_repr(task)
