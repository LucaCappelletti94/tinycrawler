"""Test if everything works in downloader task assembler."""
from tinycrawler.processes import DownloaderTaskAssembler
from tinycrawler.managers import ClientCrawlerManager
from ..managers.test_client_crawler_manager import setup as manager_setup
from ..expirables.test_url import setup as url_setup
from ..expirables.test_proxy import setup_local as setup_local_proxy
from ..commons import mock_repr, build_repr
from ..commons import sleep
from typing import Tuple
import pytest
from queue import Empty


def setup()->Tuple[DownloaderTaskAssembler, ClientCrawlerManager]:
    manager = manager_setup()
    assembler = DownloaderTaskAssembler(
        urls=manager.urls,
        proxies=manager.proxies,
        tasks=manager.downloader_tasks,
        stop=manager.end_event,
        logger=manager.logger,
        task_kwargs={},
        max_waiting_timeout=60
    )

    return assembler, manager


def test_downloader_task_assembler():
    """Test if everything works in downloader task assembler."""
    assembler, manager = setup()

    url, proxy = url_setup(), setup_local_proxy()
    manager.urls.add(url)

    manager.proxies.add(proxy)

    assembler.start()
    sleep()
    manager.end_event.set()
    assembler.join()

    task = manager.downloader_tasks.pop()

    assert (url, proxy) == task.data
    build_repr(task, "assembler")
    mock_repr(task, "assembler")


def test_downloader_task_assembler_no_url_available():
    """Test if everything works in downloader task assembler."""
    assembler, manager = setup()

    proxy = setup_local_proxy()
    manager.proxies.add(proxy)

    assembler.start()
    sleep()
    manager.end_event.set()
    assembler.join()

    with pytest.raises(Empty):
        manager.downloader_tasks.pop()

    with pytest.raises(Empty):
        manager.urls.pop()

    assert manager.proxies.pop() == proxy


def test_downloader_task_assembler_no_proxy_available():
    """Test if everything works in downloader task assembler."""
    assembler, manager = setup()

    url = url_setup()
    manager.urls.add(url)

    # Removing proxy loaded for example.
    manager.proxies.pop()

    assembler.start()
    sleep()
    manager.end_event.set()
    assembler.join()

    with pytest.raises(Empty):
        manager.downloader_tasks.pop()

    with pytest.raises(Empty):
        manager.proxies.pop()

    assert manager.urls.pop() == url
