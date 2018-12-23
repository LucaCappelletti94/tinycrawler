from tinycrawler.processes.queue_process import QueueProcess
from tinycrawler.utils import Logger
from multiprocessing import Event


def test_queue_process():
    e = Event()
    path = "logs/test_queue_process.log"
    errors = Logger(path)
    qp1 = QueueProcess(e, errors)
    qp1.start()
    qp1.join()

    qp2 = QueueProcess(e, errors)
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
