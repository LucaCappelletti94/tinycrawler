"""Test if everything works in parser task assembler."""
from tinycrawler.processes import ParserTaskAssembler
from ..managers.test_client_crawler_manager import setup as manager_setup
from ..expirables.test_response import setup as setup_response
import time


def test_parser_task_assembler():
    """Test if everything works in parser task assembler."""
    manager = manager_setup()
    assembler = ParserTaskAssembler(
        responses=manager.responses,
        tasks=manager.parser_tasks,
        stop=manager.end_event,
        logger=manager.logger,
        task_kwargs={},
        max_waiting_timeout=60
    )

    response = setup_response()
    manager.responses.add(response)

    assembler.start()
    time.sleep(2)
    manager.end_event.set()
    assembler.join()

    task = manager.parser_tasks.pop()

    assert task.response == response
