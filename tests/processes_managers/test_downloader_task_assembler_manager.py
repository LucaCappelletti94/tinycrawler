from tinycrawler.process_managers import DownloaderTaskAssemblerManager
from ..expirables.test_url import url_setup
from ..managers.test_client_crawler_manager import client_crawler_manager_setup
import pytest
from queue import Empty
from ..commons import sleep


def downloader_task_assembler_manager_setup():
    ccm = client_crawler_manager_setup()
    manager = DownloaderTaskAssemblerManager(
        stop=ccm.end_event,
        logger=ccm.logger,
        max_waiting_timeout=10,
        max_processes=8,
        tasks=ccm.downloader_tasks,
        task_kwargs={},
        urls=ccm.urls,
        proxies=ccm.proxies
    )
    return manager, ccm


def test_downloader_task_assembler_manager():
    manager, ccm = downloader_task_assembler_manager_setup()
    url = url_setup()
    ccm.urls.add(url)
    manager.update()
    sleep()
    ccm.end_event.set()
    manager.join()
    task = ccm.downloader_tasks.pop(ccm.client.ip)
    assert task.url == url.url
    with pytest.raises(Empty):
        ccm.urls.pop()
    with pytest.raises(Empty):
        ccm.proxies.pop()
