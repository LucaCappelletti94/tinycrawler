from tinycrawler.process_managers import ParserManager
from ..expirables.test_parser_task import setup as parser_task_setup
from ..managers.test_client_crawler_manager import setup as client_crawler_manager_setup
from ..commons import sleep


def setup():
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


def test_parser_manager():
    manager, ccm = setup()
    task = parser_task_setup()
    ccm.parser_tasks.add(task)
    manager.update()
    sleep()
    ccm.end_event.set()
    manager.join()
    assert ccm.completed_parser_tasks.pop() == task
