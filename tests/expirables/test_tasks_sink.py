from tinycrawler.expirables import TasksSink
from .test_downloader_task import setup as downloader_task_setup
from ..commons import mock_repr, build_repr
from .test_tasks_queue import setup as tasks_queue_setup


def setup(tq=None):
    return TasksSink(tq or tasks_queue_setup())


def test_tasks_queue():
    tq = tasks_queue_setup()
    ts = setup(tq)

    task = downloader_task_setup()

    ts.add(task)

    tq.add(task)
    ts.add(task)
    assert not tq.delete(task)

    build_repr(ts)
    mock_repr(ts)
