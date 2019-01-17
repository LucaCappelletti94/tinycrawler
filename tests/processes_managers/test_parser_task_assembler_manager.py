from tinycrawler.process_managers import ParserTaskAssemblerManager
from ..expirables.test_response import setup as response_setup
from ..managers.test_client_crawler_manager import setup as client_crawler_manager_setup
import pytest
from queue import Empty
from ..commons import sleep


def setup():
    ccm = client_crawler_manager_setup()
    manager = ParserTaskAssemblerManager(
        stop=ccm.end_event,
        logger=ccm.logger,
        max_waiting_timeout=10,
        max_processes=8,
        tasks=ccm.parser_tasks,
        task_kwargs={},
        responses=ccm.responses
    )
    return manager, ccm


def test_parser_task_assembler_manager():
    manager, ccm = setup()
    response = response_setup()
    ccm.responses.add(response)
    manager.update()
    sleep()
    ccm.end_event.set()
    manager.join()
    assert ccm.parser_tasks.pop()
    with pytest.raises(Empty):
        ccm.responses.pop()
