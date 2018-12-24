from tinycrawler.processes.server.disassembler.task_disassembler import TaskDisassembler
from tinycrawler.expirables import TasksQueue, DownloaderTask, Proxy, Url
from tinycrawler.utils import Logger, ProxyData
from multiprocessing import Event
import time
import json


def test_task_disassembler():
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

    disassembler = TaskDisassembler(
        tasks,
        stop=e,
        logger=errors
    )

    assert disassembler._source() == downloader_task
