"""Test if everything is ok with the task assembler."""
from tinycrawler.processes.server.assembler.task_assembler import TaskAssembler
from tinycrawler.expirables import TasksQueue, DownloaderTask
from multiprocessing import Event
from ..expirables.test_downloader_task import setup as downloader_task_setup
from ..utils.test_logger import setup as logger_setup


def test_task_assembler():
    """Test if everything is ok with the task assembler."""
    e = Event()
    tasks = TasksQueue()

    tasks.add(downloader_task_setup())

    TaskAssembler(
        tasks,
        stop=e,
        logger=logger_setup(),
        task_kwargs={},
        max_waiting_timeout=60
    )
