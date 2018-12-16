from tinycrawler.expirables.task.task import Task
from tinycrawler import IllegalArgumentError


def test_task_eq():
    t1 = Task(0)
    t2 = Task(0)

    assert t1 == t2


def test_task():
    task = Task(0)
    task.use()
    task.used()
    assert task.status == Task.UNASSIGNED
    task.status = Task.SUCCESS
    try:
        task.status = ["I'm not even an int."]
        assert False
    except IllegalArgumentError:
        pass

    with open("test_data/expected_task_representation.json", "r") as f:
        assert str(task) == f.read()
