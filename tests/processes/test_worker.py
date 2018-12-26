from tinycrawler.processes.client.worker import Worker
from tinycrawler.expirables import TasksQueue, DownloaderTask, Proxy, Url, ClientData
from tinycrawler.utils import Logger, ProxyData
from ..commons import mock_ip_success
from multiprocessing import Event
from httmock import HTTMock
import json


def test_worker():
    e = Event()
    path = "logs/test_queue_process.log"
    errors = Logger(path)

    tasks = TasksQueue(DownloaderTask)
    completed_tasks = TasksQueue(DownloaderTask)

    with HTTMock(mock_ip_success):
        client_data = ClientData(3)

    with open("test_data/raw_proxy_data.json", "r") as f:
        proxy_data = ProxyData(data=json.load(f))

    url = Url("https://travis-ci.org/LucaCappelletti94/tinycrawler/builds/468601955")
    proxy = Proxy(proxy_data, maximum_usages=1)

    downloader_task = DownloaderTask(proxy, url)

    tasks.add(downloader_task)

    worker = Worker(
        client_data,
        tasks,
        completed_tasks,
        stop=e,
        logger=errors
    )

    worker._sink(downloader_task)

    try:
        worker._work(None)
        assert False
    except NotImplementedError:
        pass

    assert completed_tasks.pop(client_data.ip) == downloader_task
    assert worker._source()[0] == downloader_task
