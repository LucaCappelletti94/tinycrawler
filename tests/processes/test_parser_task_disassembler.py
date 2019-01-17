"""Test if everything works in parser task disassembler."""
from tinycrawler.processes import ParserTaskDisassembler
from tinycrawler.managers import ClientCrawlerManager
from ..managers.test_client_crawler_manager import client_crawler_manager_setup
from ..expirables.test_parser_task import parser_task_setup
from ..commons import default_url
from ..commons import sleep
import os
from typing import Tuple


def parser_task_disassembler_setup()->Tuple[ParserTaskDisassembler, ClientCrawlerManager]:
    manager = client_crawler_manager_setup()
    disassembler = ParserTaskDisassembler(
        responses=manager.responses,
        tasks=manager.completed_parser_tasks,
        stop=manager.end_event,
        logger=manager.logger,
        urls=manager.urls,
        proxies=manager.proxies,
        task_kwargs={},
        max_waiting_timeout=60
    )
    return disassembler, manager


def test_parser_task_disassembler_success():
    """Test if everything works in parser task disassembler."""
    disassembler, manager = parser_task_disassembler_setup()

    task = parser_task_setup()
    task.status = task.SUCCESS
    task.urls = {default_url}
    task.page = "ICH BINE EIN BERLINER."
    task.path = "test_data/kennedy.txt"

    manager.parser_tasks.add(task)
    manager.completed_parser_tasks.add(task)

    disassembler.start()
    sleep()
    manager.end_event.set()
    disassembler.join()

    assert manager.urls.pop().url == default_url
    assert os.path.exists(task.path)
    with open(task.path, "r") as f:
        assert task.page == f.read()
    os.remove(task.path)


def test_parser_task_disassembler_failure():
    """Test if everything works in parser task disassembler."""
    disassembler, manager = parser_task_disassembler_setup()

    task = parser_task_setup()
    task.status = task.FAILURE
    task.urls = {default_url}
    task.page = "ICH BINE EIN BERLINER."
    task.path = "test_data/kennedy.txt"

    manager.parser_tasks.add(task)
    manager.completed_parser_tasks.add(task)

    disassembler.start()
    sleep()
    manager.end_event.set()
    disassembler.join()

    assert not os.path.exists(task.path)
