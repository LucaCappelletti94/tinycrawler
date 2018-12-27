from tinycrawler.processes.queue_process import QueueProcess
from multiprocessing import Event
from ..utils.test_logger import setup as logger_setup


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

    try:
        qp1._source()
        assert False
    except NotImplementedError:
        pass

    try:
        qp1._job()
        assert False
    except NotImplementedError:
        pass

    try:
        qp1._sink()
        assert False
    except NotImplementedError:
        pass
