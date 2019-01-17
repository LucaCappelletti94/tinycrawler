from tinycrawler.processes.queue_process import QueueProcess
from multiprocessing import Event
from ..utils.test_logger import logger_setup
import pytest


def test_queue_process():
    e = Event()
    errors = logger_setup()
    qp1 = QueueProcess(e, errors, 60)
    qp1.start()
    qp1.join()

    qp2 = QueueProcess(e, errors, 60)
    e.set()
    qp2.start()
    qp2.join()

    with pytest.raises(NotImplementedError):
        qp1._source()

    with pytest.raises(NotImplementedError):
        qp1._job()

    with pytest.raises(NotImplementedError):
        qp1._sink()
