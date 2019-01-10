from tinycrawler.expirables import TasksQueue, Domain
from queue import Empty
from .test_downloader_task import setup as downloader_task_setup
from ..commons import mock_repr, build_repr
import pytest


def setup():
    return TasksQueue()


def test_tasks_queue():
    tq = setup()

    task = downloader_task_setup()

    ip = Domain("12.121.121.33")
    ip2 = Domain("12.121.121.38")
    tq.add(task, ip=ip)

    # Should raise Empty because no task was given either at the ip `ip2`
    with pytest.raises(Empty):
        tq.pop(ip=ip2)

    assert tq.pop(ip=ip) == task

    # Should raise Empty because there are no tasks with True `is_available` with given ip.
    with pytest.raises(Empty):
        tq.pop(ip=ip)

    task.used(success=True)
    tq.add(task)

    assert tq.pop(ip=ip2) == task

    tq.add(task)
    build_repr(tq)
    mock_repr(tq)
