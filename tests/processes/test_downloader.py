from tinycrawler.expirables import TasksQueue, DownloaderTask
from tinycrawler.processes import Downloader
from multiprocessing import Event
import requests
from httmock import HTTMock, urlmatch, response
from typing import Tuple
import time
from ..expirables.test_downloader_task import setup as downloader_task_setup
from ..utils.test_logger import setup as logger_setup
from ..expirables.test_client_data import setup as client_data_setup
from ..expirables.test_expirables_queue import setup as expirables_queue_setup
from ..managers.test_client_crawler_manager import setup as client_crawler_manager_setup


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
    manager = client_crawler_manager_setup()
    tasks = manager.downloader_tasks
    completed_tasks = manager.completed_downloader_tasks

    tasks.add(downloader_task_setup())
    completed_tasks.add(downloader_task_setup())

    return Downloader(
        max_content_len=10000,
        user_agent="*",
        email="myemail@email.com",
        client_data=client_data_setup(),
        tasks=tasks,
        completed_tasks=completed_tasks,
        stop=e,
        logger=logger_setup(),
        max_waiting_timeout=1
    ), tasks, completed_tasks, e


def test_downloader_success():
    with HTTMock(mock_downloader_success):
        downloader, _, completed_tasks, e = setup_downloader()
        # downloader.start()
        # time.sleep(0.5)
        # e.set()
        # downloader.join()
        downloader._loop()
        completed = completed_tasks.pop()
        assert completed.text == expected_successful_download()
        assert completed.status == DownloaderTask.SUCCESS
        assert not completed.binary


# def test_downloader_success_empty():
#     with HTTMock(mock_downloader_success_empty):
#         downloader, _, completed_tasks, e = setup_downloader()
#         downloader.start()
#         time.sleep(0.5)
#         e.set()
#         downloader.join()
#         completed = completed_tasks.pop()
#         assert completed.text == ""
#         assert completed.status == DownloaderTask.SUCCESS
#         assert not completed.binary


# def test_downloader_success_binary():
#     with HTTMock(mock_downloader_success_binary):
#         downloader, _, completed_tasks, e = setup_downloader()
#         downloader.start()
#         time.sleep(0.5)
#         e.set()
#         downloader.join()
#         completed = completed_tasks.pop()
#         assert completed.status == DownloaderTask.SUCCESS
#         assert completed.binary


# def test_downloader_success_small_binary():
#     with HTTMock(mock_downloader_success_small_binary):
#         downloader, _, completed_tasks, e = setup_downloader()
#         downloader.start()
#         time.sleep(0.5)
#         e.set()
#         downloader.join()
#         completed = completed_tasks.pop()
#         assert completed.status == DownloaderTask.SUCCESS
#         assert completed.binary


# def test_downloader_failure():
#     with HTTMock(mock_downloader_failure):
#         downloader, _, completed_tasks, e = setup_downloader()
#         downloader.start()
#         time.sleep(0.5)
#         e.set()
#         downloader.join()
#         completed = completed_tasks.pop()
#         assert completed.status == DownloaderTask.FAILURE


# def test_downloader_failure_max_size():
#     with HTTMock(mock_downloader_failure_max_size):
#         downloader, _, completed_tasks, e = setup_downloader()
#         downloader.start()
#         time.sleep(0.5)
#         e.set()
#         downloader.join()
#         completed = completed_tasks.pop()
#         assert completed.status == DownloaderTask.FAILURE
