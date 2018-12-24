from tinycrawler.expirables import DownloaderTask, Proxy
from tinycrawler.utils import ProxyData
from tinycrawler import Url
import json


def test_downloader_task():
    with open("test_data/raw_proxy_data.json", "r") as f:
        proxy_data = ProxyData(data=json.load(f))

    url = Url("https://travis-ci.org/LucaCappelletti94/tinycrawler/builds/468601955")
    proxy = Proxy(proxy_data, maximum_usages=1)

    downloader_task = DownloaderTask(proxy, url)
    downloader_task.task_id = 0

    assert downloader_task.url == url.url
    assert downloader_task.proxy == proxy.data

    downloader_task.use()
    downloader_task.used(True)

    try:
        downloader_task.text
        assert False
    except ValueError:
        pass

    try:
        downloader_task.response_status
        assert False
    except ValueError:
        pass

    try:
        downloader_task.binary
        assert False
    except ValueError:
        pass

    text = "test/my_file.txt"
    response_status = 200

    downloader_task.text = text

    try:
        downloader_task.text = text
    except ValueError:
        pass

    downloader_task.binary = True

    try:
        downloader_task.binary = True
    except ValueError:
        pass

    downloader_task.response_status = response_status

    try:
        downloader_task.response_status = response_status
    except ValueError:
        pass

    assert downloader_task.text == text
    assert downloader_task.response_status == response_status
    assert downloader_task.binary

    with open("test_data/expected_downloader_task_representation.json", "r") as f:
        assert str(downloader_task) == f.read()
