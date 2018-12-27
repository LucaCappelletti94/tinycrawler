"""Test if everything is ok with the worker."""
from tinycrawler.processes.client.worker import Worker
from tinycrawler.expirables import TasksQueue, DownloaderTask
from multiprocessing import Event
from ..expirables.test_downloader_task import setup as downloader_task_setup
from ..expirables.test_client_data import setup as client_data_setup
from ..utils.test_logger import setup as logger_setup


def test_worker():
    """Test if everything is ok with the worker."""
    e = Event()

    tasks = TasksQueue(DownloaderTask)
    completed_tasks = TasksQueue(DownloaderTask)

    tasks.add(downloader_task_setup())

    worker = Worker(
        client_data=client_data_setup(),
        tasks=tasks,
        completed_tasks=completed_tasks,
        stop=e,
        logger=logger_setup(),
        max_waiting_timeout=60
    )

    try:
        worker._work(None)
        assert False
    except NotImplementedError:
        pass
