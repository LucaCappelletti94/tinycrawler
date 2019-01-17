from tinycrawler.process_managers import DownloaderTaskDisassemblerManager
from .test_downloader_manager import run_downloader_manager
import pytest
from queue import Empty
from ..commons import sleep


def downloader_task_assembler_manager_setup():
    ccm = run_downloader_manager()
    ccm.end_event.clear()
    manager = DownloaderTaskDisassemblerManager(
        stop=ccm.end_event,
        logger=ccm.logger,
        max_waiting_timeout=10,
        max_processes=8,
        tasks=ccm.completed_downloader_tasks,
        urls=ccm.urls,
        proxies=ccm.proxies,
        responses=ccm.responses
    )
    return manager, ccm


def test_downloader_task_assembler_manager():
    manager, ccm = downloader_task_assembler_manager_setup()
    manager.update()
    sleep()
    ccm.end_event.set()
    manager.join()
    with pytest.raises(Empty):
        ccm.completed_downloader_tasks.pop()
