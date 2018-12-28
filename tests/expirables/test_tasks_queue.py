from tinycrawler.expirables import TasksQueue, DownloaderTask, Domain
from queue import Empty
from .test_downloader_task import setup as downloader_task_setup
from ..commons import mock_repr
import pytest


def setup():
    return TasksQueue(DownloaderTask)


def test_tasks_queue():
    tq = setup()
    with pytest.raises(AssertionError):
        TasksQueue(str)

    task = downloader_task_setup()

    ip = Domain("12.121.121.33")
    ip2 = Domain("12.121.121.38")
    tq.add(task, ip=ip)

    with pytest.raises(Empty):
        tq.pop(ip=ip2)

    assert tq.pop(ip=ip) == task

    with pytest.raises(Empty):
        tq.pop(ip=ip)

    tq.add(task)

    assert tq.pop(ip=ip2) == task

    tq.add(task)
    mock_repr(tq)
