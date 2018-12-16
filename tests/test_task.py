from tinycrawler.expirables.task.task import Task
from tinycrawler import IllegalArgumentError


def test_task_eq():
    t1 = Task(0)
    t2 = Task(0)

    assert t1 == t2


def test_task():
    t = Task(0)
    t.use()
    t.used()
    assert t.status == Task.UNASSIGNED
    t.status = Task.SUCCESS
    try:
        t.status = ["I'm not even an int."]
        assert False
    except IllegalArgumentError:
        pass

    print(t)

    with open("test_data/expected_task_representation.json", "r") as f:
        assert str(t) == f.read()
