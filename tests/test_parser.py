from tinycrawler.expirables import TasksQueue, ParserTask, ClientData, Response
from tinycrawler.processes import Parser
from tinycrawler.utils import Logger
from multiprocessing import Event
from .commons import mock_ip_success
from httmock import HTTMock
from typing import Tuple


def setup_parser()->Tuple[Parser, TasksQueue, TasksQueue]:
    e = Event()
    path = "logs/test_queue_process.log"
    errors = Logger(path)

    tasks = TasksQueue(ParserTask)
    completed_tasks = TasksQueue(ParserTask)

    with HTTMock(mock_ip_success):
        client_data = ClientData(3)

    url = "https://requests-mock.readthedocs.io/en/latest/response.html"
    with open("test_data/successfull_download.html", "r") as f:
        content = f.read()
    status = 200

    response = Response(content, status, url)
    parser_task = ParserTask(response)
    parser_task.use()

    tasks.add(parser_task)

    return Parser(
        client_data=client_data,
        tasks=tasks,
        completed_tasks=completed_tasks,
        stop=e,
        logger=errors
    ), tasks, completed_tasks


def test_parser_success():
    parser, _, completed_tasks = setup_parser()
    parser._loop()
    completed = completed_tasks.pop()
    assert completed.status == ParserTask.SUCCESS


def invalid_path(url: str):
    raise Exception()


def test_parser_failure():
    parser, _, completed_tasks = setup_parser()
    parser._path = invalid_path
    parser._loop()
    completed = completed_tasks.pop()
    assert completed.status == ParserTask.FAILURE
