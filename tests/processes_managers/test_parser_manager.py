from tinycrawler.process_managers import ParserManager
from ..expirables.test_parser_task import parser_task_setup
from ..managers.test_client_crawler_manager import client_crawler_manager_setup
from ..commons import sleep


def parser_manager_setup():
    ccm = client_crawler_manager_setup()
    manager = ParserManager(
        stop=ccm.end_event,
        logger=ccm.logger,
        max_waiting_timeout=10,
        max_processes=8,
        client_data=ccm.client,
        tasks=ccm.parser_tasks,
        completed_tasks=ccm.completed_parser_tasks,
        page=None,
        path=None,
        url=None
    )
    return manager, ccm


def run_parser_manager(task=None):
    manager, ccm = parser_manager_setup()
    task = task or parser_task_setup()
    ccm.parser_tasks.add(task)
    manager.update()
    sleep()
    ccm.end_event.set()
    manager.join()
    return ccm


def test_parser_manager():
    task = parser_task_setup()
    ccm = run_parser_manager(task)
    assert ccm.completed_parser_tasks.pop() == task
