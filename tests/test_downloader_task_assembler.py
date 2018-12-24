from tinycrawler.processes import DownloaderTaskAssembler
from tinycrawler.data import Urls
from tinycrawler.expirables import TasksQueue, DownloaderTask, Proxy, Url
from tinycrawler.utils import Logger, ProxyData
from multiprocessing import Event
from httpretty import httprettified
from .utils import mock_robots, build_default_url
from tinycrawler.data import Proxies
import time
import json


@httprettified
def test_downloader_task_assembler():
    mock_robots()

    urls = Urls(
        bloom_filter_capacity=10000,
        follow_robot_txt=True,
        useragent="*",
        default_url_timeout=1,
        robots_timeout=0
    )

    urls.add(
        set([Url(build_default_url("/error"), use_timeout=5)]))

    proxies = Proxies(path="test_data/raw_proxies.json")

    e = Event()
    path = "logs/test_queue_process.log"
    errors = Logger(path)

    tasks = TasksQueue(DownloaderTask)

    with open("test_data/raw_proxy_data.json", "r") as f:
        proxy_data = ProxyData(data=json.load(f))

    url = Url("https://travis-ci.org/LucaCappelletti94/tinycrawler/builds/468601955")
    proxy = Proxy(proxy_data, maximum_usages=1)

    downloader_task = DownloaderTask(proxy, url)

    tasks.add(downloader_task)

    assembler = DownloaderTaskAssembler(
        urls,
        proxies,
        tasks=tasks,
        stop=e,
        logger=errors
    )

    assembler.start()
    time.sleep(0.5)
    e.set()
    assembler.join()

    assert tasks.pop() == downloader_task
