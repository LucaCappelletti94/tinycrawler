from tinycrawler.process_managers import DownloaderManager
from ..managers.test_client_crawler_manager import setup as client_crawler_manager_setup


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
    manager.update()
