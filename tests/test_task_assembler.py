from tinycrawler.processes.server.assembler.task_assembler import TaskAssembler
from tinycrawler.expirables import TasksQueue, DownloaderTask, Proxy, Url
from tinycrawler.utils import Logger, ProxyData
from multiprocessing import Event
import json


def test_task_assembler():
    e = Event()
    path = "logs/test_queue_process.log"
    errors = Logger(path)

    tasks = TasksQueue(DownloaderTask)

    with open("test_data/raw_proxy_data.json", "r") as f:
        proxy_data = ProxyData(data=json.load(f))

    url = Url("https://travis-ci.org/LucaCappelletti94/tinycrawler/builds/468601955")
    proxy = Proxy(proxy_data, maximum_usages=1)

    downloader_task = DownloaderTask(proxy, url, 0)

    tasks.add(downloader_task)

    assembler = TaskAssembler(
        tasks,
        stop=e,
        logger=errors
    )

    assembler._sink(downloader_task)

    assert tasks.pop() == downloader_task
