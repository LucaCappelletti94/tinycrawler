from tinycrawler.expirables.task.task import Task
from tinycrawler import IllegalArgumentError


def test_task_eq():
    t1 = Task()
    t2 = Task()
    t1.task_id = t2.task_id = 3

    assert t1 == t2


def test_task():
    task = Task()
    try:
        task.task_id
        assert False
    except IllegalArgumentError:
        pass
    task.task_id = 0
    try:
        task.task_id = 0
        assert False
    except IllegalArgumentError:
        pass
    task.use()
    task.used()
    assert task.status == Task.UNASSIGNED
    task.status = Task.SUCCESS
    try:
        task.status = "Lo kebabbo non devi manducare."
        assert False
    except IllegalArgumentError:
        pass

    with open("test_data/expected_task_representation.json", "r") as f:
        assert str(task) == f.read()
