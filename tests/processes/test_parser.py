from tinycrawler.expirables import TasksQueue, ParserTask
from tinycrawler.processes import Parser
from multiprocessing import Event
from typing import Tuple
from ..expirables.test_parser_task import setup as parser_task_setup
from ..utils.test_logger import setup as logger_setup
from ..expirables.test_client_data import setup as client_data_setup
import time
from ..commons import mock_repr
from ..managers.test_client_crawler_manager import setup as client_crawler_manager_setup


def setup(page=None)->Tuple[Parser, TasksQueue, TasksQueue, Event]:
    e = Event()

    manager = client_crawler_manager_setup()

    tasks = manager.parser_tasks
    completed_tasks = manager.completed_parser_tasks

    task = parser_task_setup()
    tasks.add(task)

    return Parser(
        client_data=client_data_setup(),
        page=page,
        tasks=tasks,
        completed_tasks=completed_tasks,
        stop=e,
        logger=logger_setup(),
        max_waiting_timeout=60
    ), tasks, completed_tasks, e


def test_parser():
    parser, _, completed_tasks, e = setup()
    parser.start()
    time.sleep(2)
    e.set()
    parser.join()
    completed = completed_tasks.pop()
    mock_repr(completed, "parser")
    assert completed.status == ParserTask.SUCCESS


def fail(*args):
    raise Exception


def test_parser_failure():
    parser, _, completed_tasks, e = setup(
        page=fail
    )
    parser.start()
    time.sleep(2)
    e.set()
    parser.join()
    completed = completed_tasks.pop()
    assert completed.status == ParserTask.FAILURE
