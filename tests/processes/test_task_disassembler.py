"""Test if everything is ok with the task disassembler."""
from tinycrawler.processes.server.disassembler.task_disassembler import TaskDisassembler
from tinycrawler.expirables import TasksQueue
from multiprocessing import Event
from ..expirables.test_downloader_task import downloader_task_setup
from ..utils.test_logger import logger_setup


def test_task_disassembler():
    """Test if everything is ok with the task disassembler."""
    e = Event()
    tasks = TasksQueue()

    tasks.add(downloader_task_setup())

    TaskDisassembler(
        tasks,
        stop=e,
        logger=logger_setup(),
        max_waiting_timeout=60
    )
