"""Test if everything is ok with the worker."""
from tinycrawler.processes.client.worker import Worker
from tinycrawler.expirables import TasksQueue
from multiprocessing import Event
from ..expirables.test_downloader_task import downloader_task_setup
from ..expirables.test_client_data import client_data_setup
from ..utils.test_logger import logger_setup
import pytest


def test_worker():
    """Test if everything is ok with the worker."""
    e = Event()

    tasks = TasksQueue()
    completed_tasks = TasksQueue()

    tasks.add(downloader_task_setup())

    worker = Worker(
        client_data=client_data_setup(),
        tasks=tasks,
        completed_tasks=completed_tasks,
        stop=e,
        logger=logger_setup(),
        max_waiting_timeout=60
    )

    with pytest.raises(NotImplementedError):
        worker._work(None)
