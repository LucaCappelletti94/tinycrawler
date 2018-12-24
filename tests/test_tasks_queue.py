from tinycrawler.expirables import TasksQueue, DownloaderTask, Domain
from tinycrawler import IllegalArgumentError
from queue import Empty


def test_tasks_queue():
    tq = TasksQueue(DownloaderTask)
    try:
        TasksQueue(str)
        assert False
    except IllegalArgumentError:
        pass
    task = DownloaderTask(None, None)

    ip = Domain("12.121.121.33")
    ip2 = Domain("12.121.121.38")
    tq.add(task, ip=ip)

    try:
        tq.pop(ip=ip2)
        assert False
    except Empty:
        pass

    assert tq.pop(ip=ip) == task

    try:
        tq.pop(ip=ip)
        assert False
    except Empty:
        pass

    tq.add(task)

    assert tq.pop(ip=ip2) == task

    tq.add(task)

    with open("test_data/expected_tasks_queue_representation.json", "r") as f:
        assert str(tq) == f.read()
