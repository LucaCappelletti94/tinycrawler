from tinycrawler.process_managers import DownloaderManager
from ..expirables.test_downloader_task import local_setup as downloader_task_setup
from ..managers.test_client_crawler_manager import setup as client_crawler_manager_setup
from ..processes.test_downloader import mock_downloader_success
from httmock import HTTMock
import time


def setup():
    ccm = client_crawler_manager_setup()
    manager = DownloaderManager(
        stop=ccm.end_event,
        logger=ccm.logger,
        max_waiting_timeout=10,
        max_processes=8,
        client_data=ccm.client,
        tasks=ccm.downloader_tasks,
        completed_tasks=ccm.completed_downloader_tasks,
        max_content_len=1000,
        user_agent="*",
        email="ho@hoho.it"
    )
    return manager, ccm


def test_downloader_manager():
    manager, ccm = setup()
    task = downloader_task_setup()
    ccm.downloader_tasks.add(task)
    with HTTMock(mock_downloader_success):
        manager.update()
        time.sleep(2)
        ccm.end_event.set()
        manager.join()
        assert ccm.completed_downloader_tasks.pop() == task
