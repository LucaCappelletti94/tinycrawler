from tinycrawler.processes import ParserTaskAssembler
from tinycrawler.expirables import TasksQueue, ParserTask, ExpirablesQueue, Response
from tinycrawler.utils import Logger
from multiprocessing import Event
from httpretty import httprettified
from ..expirables.test_response import setup as response_setup
import time


@httprettified
def test_downloader_task_assembler():
    responses = ExpirablesQueue(Response)

    responses.add(response_setup())

    e = Event()
    path = "logs/test_queue_process.log"
    errors = Logger(path)

    tasks = TasksQueue(ParserTask)

    assembler = ParserTaskAssembler(
        responses,
        tasks=tasks,
        stop=e,
        logger=errors,
        task_kwargs={}
    )

    assembler.start()
    time.sleep(0.5)
    e.set()
    assembler.join()
