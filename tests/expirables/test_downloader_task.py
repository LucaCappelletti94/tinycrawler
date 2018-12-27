from tinycrawler.expirables import DownloaderTask
from .test_proxy import setup as proxy_setup, setup_local as proxy_setup_local
from .test_url import setup as url_setup
from ..commons import mock_repr


def setup(proxy=None, url=None)->DownloaderTask:
    proxy = proxy or proxy_setup()
    url = url or url_setup()
    task = DownloaderTask(proxy, url)
    task.task_id = 0
    return task


def local_setup(proxy=None, url=None)->DownloaderTask:
    proxy = proxy or proxy_setup_local()
    url = url or url_setup()
    task = DownloaderTask(proxy, url)
    task.task_id = 0
    return task


def test_downloader_task():
    proxy = proxy_setup()
    url = url_setup()
    downloader_task = setup(proxy, url)

    assert downloader_task.url == url.url
    assert downloader_task.proxy == proxy.data

    downloader_task.use()
    downloader_task.used(
        success=True
    )

    text = "test/my_file.txt"
    response_status = 200

    downloader_task.text = text

    try:
        downloader_task.text = text
    except AssertionError:
        pass

    downloader_task.binary = True

    try:
        downloader_task.binary = True
    except AssertionError:
        pass

    downloader_task.response_status = response_status

    try:
        downloader_task.response_status = response_status
    except AssertionError:
        pass

    assert downloader_task.text == text
    assert downloader_task.response_status == response_status
    assert downloader_task.binary


def test_downloader_task_repr():
    mock_repr(setup())
