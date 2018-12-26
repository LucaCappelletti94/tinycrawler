from tinycrawler.expirables import TasksQueue, DownloaderTask, Domain
from queue import Empty
from .test_proxy import setup as proxy_setup
from .test_url import setup as url_setup


def test_tasks_queue():
    tq = TasksQueue(DownloaderTask)
    try:
        TasksQueue(str)
        assert False
    except AssertionError:
        pass
    task = DownloaderTask(proxy_setup(), url_setup())

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
