from tinycrawler.expirables import DownloaderTask, Response, Proxy
from tinycrawler.utils import ProxyData
from tinycrawler import Url, Domain
import json
from .utils import double_arguments_test


def test_downloader_task_arguments():
    with open("test_data/raw_proxy_data.json", "r") as f:
        proxy_data = ProxyData(json.load(f))

    domain = Domain("78.38.241.9")
    url = Url("https://travis-ci.org/LucaCappelletti94/tinycrawler/builds/468601955")
    proxy = Proxy(domain, proxy_data, maximum_usages=1)

    downloader_task = DownloaderTask(proxy, url, 0)

    downloader_task.url
    downloader_task.proxy

    downloader_task.use()
    downloader_task.used(True)

    try:
        downloader_task.response
    except ValueError:
        pass

    try:
        downloader_task.binary
    except ValueError:
        pass

    downloader_task.response = "test/my_file.txt"

    try:
        downloader_task.response = "test/my_file.txt"
    except ValueError:
        pass

    downloader_task.binary = True

    downloader_task.response
    downloader_task.binary

    with open("test_data/expected_downloader_task_representation.json", "r") as f:
        assert str(downloader_task) == f.read()
