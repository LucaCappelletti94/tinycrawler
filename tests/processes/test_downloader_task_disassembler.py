"""Test if everything works in downloader task disassembler."""
from tinycrawler.processes import DownloaderTaskDisassembler
from tinycrawler.managers import ClientCrawlerManager
from ..expirables.test_downloader_task import setup as setup_downloader_task
from ..managers.test_client_crawler_manager import setup as manager_setup
from ..commons import mock_repr
from typing import Tuple
from queue import Empty
from ..commons import sleep
import pytest


def expected_successful_download()->str:
    with open("test_data/successfull_download.html", "r") as f:
        return f.read()


def setup()->Tuple[DownloaderTaskDisassembler, ClientCrawlerManager]:
    manager = manager_setup()
    disassembler = DownloaderTaskDisassembler(
        urls=manager.urls,
        proxies=manager.proxies,
        responses=manager.responses,
        tasks=manager.completed_downloader_tasks,
        stop=manager.end_event,
        logger=manager.logger,
        task_kwargs={},
        max_waiting_timeout=60
    )
    return disassembler, manager


def test_downloader_task_disassembler_success():
    """Test if everything works in downloader task disassembler on occasion of success."""
    disassembler, manager = setup()

    task = setup_downloader_task()
    task.status = task.SUCCESS
    task.binary = False
    task.response_status = 200
    task.text = expected_successful_download()
    manager.downloader_tasks.add(task)
    manager.completed_downloader_tasks.add(task)

    url, _ = task.data

    # Removing the proxy put by default for example in manager
    manager.proxies.pop(url.domain)

    disassembler.start()
    sleep()
    manager.end_event.set()
    disassembler.join()

    with pytest.raises(Empty):
        manager.urls.pop()

    with pytest.raises(Empty):
        manager.proxies.pop(url.domain)

    response = manager.responses.pop()
    mock_repr(response, "disassembler")


def test_downloader_task_disassembler_binary():
    """Test if everything works in downloader task disassembler on occasion of success."""
    disassembler, manager = setup()

    task = setup_downloader_task()
    task.status = task.SUCCESS
    task.binary = True
    task.response_status = 200
    manager.downloader_tasks.add(task)
    manager.completed_downloader_tasks.add(task)

    url, _ = task.data

    # Removing the proxy put by default for example in manager
    manager.proxies.pop(url.domain)

    disassembler.start()
    sleep()
    manager.end_event.set()
    disassembler.join()

    with pytest.raises(Empty):
        manager.urls.pop()

    with pytest.raises(Empty):
        manager.proxies.pop(url.domain)

    with pytest.raises(Empty):
        manager.responses.pop()


def test_downloader_task_disassembler_failure():
    """Test if everything works in downloader task disassembler on occasion of failure."""
    disassembler, manager = setup()

    task = setup_downloader_task()
    task.status = task.FAILURE
    manager.downloader_tasks.add(task)
    manager.completed_downloader_tasks.add(task)

    disassembler.start()
    sleep()
    manager.end_event.set()
    disassembler.join()

    url, proxy = task.data
    assert manager.urls.pop() == url
    assert manager.proxies.pop(url.domain) == proxy
