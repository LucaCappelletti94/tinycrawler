"""Test if everything works in parser task assembler."""
from tinycrawler.processes import ParserTaskAssembler
from ..managers.test_client_crawler_manager import client_crawler_manager_setup
from ..expirables.test_response import response_setup
from ..commons import sleep


def test_parser_task_assembler():
    """Test if everything works in parser task assembler."""
    manager = client_crawler_manager_setup()
    assembler = ParserTaskAssembler(
        responses=manager.responses,
        tasks=manager.parser_tasks,
        stop=manager.end_event,
        logger=manager.logger,
        task_kwargs={},
        max_waiting_timeout=60
    )

    response = response_setup()
    manager.responses.add(response)

    assembler.start()
    sleep()
    manager.end_event.set()
    assembler.join()

    task = manager.parser_tasks.pop()

    assert task.response == response
