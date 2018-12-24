from tinycrawler.processes.server.disassembler.task_disassembler import TaskDisassembler
from tinycrawler.expirables import TasksQueue, DownloaderTask, Proxy, Url, ClientData
from tinycrawler.utils import Logger, ProxyData
from .utils import mock_ip_success
from multiprocessing import Event
from httmock import HTTMock
import json


def test_task_disassembler():
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

    downloader_task = DownloaderTask(proxy, url, 0)

    tasks.add(downloader_task)

    disassembler = TaskDisassembler(
        tasks,
        stop=e,
        logger=errors
    )

    assert disassembler._source() == downloader_task
