from tinycrawler.expirables import TasksQueue, DownloaderTask, Proxy, Url, ClientData
from tinycrawler.processes import Downloader
from tinycrawler.utils import Logger, ProxyData
from ..commons import mock_ip_success
from multiprocessing import Event
import requests
from httmock import HTTMock, urlmatch, response
from typing import Tuple
import json


def expected_successful_download()->str:
    with open("test_data/successfull_download.html", "r") as f:
        return f.read()


@urlmatch(netloc=r'\.*(totallyfakewebsite.com)')
def mock_downloader_success(*args):
    """Method to mock successful downloader request."""
    return response(content=expected_successful_download())


@urlmatch(netloc=r'\.*(totallyfakewebsite.com)')
def mock_downloader_success_empty(*args):
    """Method to mock successful downloader request."""
    return response(content="")


@urlmatch(netloc=r'\.*(totallyfakewebsite.com)')
def mock_downloader_success_binary(*args):
    """Method to mock successful binary downloader request."""
    with open("test_data/binary_file.jpg", 'rb') as f:
        return response(content=f.read())


@urlmatch(netloc=r'\.*(totallyfakewebsite.com)')
def mock_downloader_success_small_binary(*args):
    """Method to mock successful small binary downloader request."""
    with open("test_data/binary_file.jpg", 'rb') as f:
        return response(content=f.read()[:100])


@urlmatch(netloc=r'\.*(totallyfakewebsite.com)')
def mock_downloader_failure(*args):
    """Method to mock failed downloader request."""
    raise requests.ConnectionError


@urlmatch(netloc=r'\.*(totallyfakewebsite.com)')
def mock_downloader_failure_max_size(*args):
    """Method to mock failed downloader request for too big file."""
    return response(content=expected_successful_download(), headers={"Content-Length": 100000})


def setup_downloader()->Tuple[Downloader, TasksQueue, TasksQueue]:
    e = Event()
    path = "logs/test_queue_process.log"
    errors = Logger(path)

    tasks = TasksQueue(DownloaderTask)
    completed_tasks = TasksQueue(DownloaderTask)

    with HTTMock(mock_ip_success):
        client_data = ClientData(3)

    with open("test_data/raw_proxy_data.json", "r") as f:
        proxy_data = ProxyData(data=json.load(f))

    url = Url("https://totallyfakewebsite.com")
    proxy = Proxy(proxy_data, maximum_usages=1)

    downloader_task = DownloaderTask(proxy, url)

    tasks.add(downloader_task)

    return Downloader(
        max_content_len=10000,
        user_agent="*",
        email="myemail@email.com",
        client_data=client_data,
        tasks=tasks,
        completed_tasks=completed_tasks,
        stop=e,
        logger=errors
    ), tasks, completed_tasks


def test_downloader_success():
    with HTTMock(mock_downloader_success):
        downloader, _, completed_tasks = setup_downloader()
        downloader._loop()
        completed = completed_tasks.pop()
        assert completed.text == expected_successful_download()
        assert completed.status == DownloaderTask.SUCCESS
        assert not completed.binary


def test_downloader_success_empty():
    with HTTMock(mock_downloader_success_empty):
        downloader, _, completed_tasks = setup_downloader()
        downloader._loop()
        completed = completed_tasks.pop()
        assert completed.text == ""
        assert completed.status == DownloaderTask.SUCCESS
        assert not completed.binary


def test_downloader_success_binary():
    with HTTMock(mock_downloader_success_binary):
        downloader, _, completed_tasks = setup_downloader()
        downloader._loop()
        completed = completed_tasks.pop()
        assert completed.status == DownloaderTask.SUCCESS
        assert completed.binary


def test_downloader_success_small_binary():
    with HTTMock(mock_downloader_success_small_binary):
        downloader, _, completed_tasks = setup_downloader()
        downloader._loop()
        completed = completed_tasks.pop()
        assert completed.status == DownloaderTask.SUCCESS
        assert completed.binary


def test_downloader_failure():
    with HTTMock(mock_downloader_failure):
        downloader, _, completed_tasks = setup_downloader()
        downloader._loop()
        completed = completed_tasks.pop()
        assert completed.status == DownloaderTask.FAILURE


def test_downloader_failure_max_size():
    with HTTMock(mock_downloader_failure_max_size):
        downloader, _, completed_tasks = setup_downloader()
        downloader._loop()
        completed = completed_tasks.pop()
        assert completed.status == DownloaderTask.FAILURE
