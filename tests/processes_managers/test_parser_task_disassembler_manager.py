from tinycrawler.process_managers import ParserTaskDisassemblerManager
from .test_parser_manager import run_parser_manager
import pytest
from queue import Empty
from ..commons import sleep
import shutil


def parser_task_assembler_manager_setup():
    ccm = run_parser_manager()
    ccm.end_event.clear()
    manager = ParserTaskDisassemblerManager(
        stop=ccm.end_event,
        logger=ccm.logger,
        max_waiting_timeout=10,
        max_processes=8,
        tasks=ccm.completed_parser_tasks,
        urls=ccm.urls,
        proxies=ccm.proxies,
        responses=ccm.responses
    )
    return manager, ccm


def test_parser_task_assembler_manager():
    manager, ccm = parser_task_assembler_manager_setup()
    manager.update()
    sleep()
    ccm.end_event.set()
    manager.join()
    with pytest.raises(Empty):
        ccm.completed_parser_tasks.pop()
    shutil.rmtree("docs.python-requests.org")
