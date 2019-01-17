from tinycrawler.process_managers.queue_process_manager import QueueProcessManager
from ..managers.test_client_crawler_manager import client_crawler_manager_setup
import pytest


def parser_manager_setup():
    ccm = client_crawler_manager_setup()
    manager = QueueProcessManager(
        stop=ccm.end_event,
        logger=ccm.logger,
        max_waiting_timeout=10,
        max_processes=8
    )
    return manager, ccm


def test_parser_manager():
    manager, _ = parser_manager_setup()
    with pytest.raises(NotImplementedError):
        manager.spawn()
    with pytest.raises(NotImplementedError):
        manager.can_spawn()
