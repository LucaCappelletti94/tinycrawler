"""Test if everything works in downloader task assembler."""
from tinycrawler.processes import DownloaderTaskAssembler
from ..managers.test_client_crawler_manager import setup as manager_setup
from ..expirables.test_url import setup as url_setup
from ..expirables.test_proxy import setup_local as setup_local_proxy
from ..commons import mock_repr
import time


def test_downloader_task_assembler():
    """Test if everything works in downloader task assembler."""
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

    url, proxy = url_setup(), setup_local_proxy()
    manager.urls.add([url])

    manager.proxies.add(proxy)

    assembler.start()
    time.sleep(0.5)
    manager.end_event.set()
    assembler.join()

    task = manager.downloader_tasks.pop()

    assert (url, proxy) == task.data
    mock_repr(task, "assembler")
