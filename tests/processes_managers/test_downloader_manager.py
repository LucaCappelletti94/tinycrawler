from tinycrawler.process_managers import DownloaderManager
from ..expirables.test_downloader_task import local_setup as downloader_task_setup
from ..managers.test_client_crawler_manager import client_crawler_manager_setup
from ..processes.test_downloader import mock_downloader_success
from ..commons import sleep
from httmock import HTTMock


def downloader_manager_setup():
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


def run_downloader_manager(task=None):
    manager, ccm = downloader_manager_setup()
    task = task or downloader_task_setup()
    ccm.downloader_tasks.add(task)
    with HTTMock(mock_downloader_success):
        manager.update()
        sleep()
        ccm.end_event.set()
        manager.join()
    return ccm


def test_downloader_manager():
    task = downloader_task_setup()
    ccm = run_downloader_manager(task)
    assert ccm.completed_downloader_tasks.pop() == task
