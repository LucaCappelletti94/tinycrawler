import logging
from multiprocessing import Lock


class Log:
    def __init__(self, directory):
        self._lock = Lock()
        self._path = "%s/error.log" % (directory)
        logging.basicConfig(filename=self._path)
        with open(self._path, 'w'):
            pass

    def log(self, message):
        """Log message with lock semaphore in info level."""
        self._lock.acquire()
        logging.info(message)
        # TODO remove this ugly commented code
        # with open(self._path, "r") as f:
        #     data = f.read()
        # with open(self._path, "w") as f:
        #     f.write(data + "\n" + message)
        self._lock.release()

    def error(self, message):
        """Log message with lock semaphore in error level."""
        self._lock.acquire()
        logging.error(message)
        # TODO remove this ugly commented code
        # with open(self._path, "r") as f:
        #     data = f.read()
        # with open(self._path, "w") as f:
        #     f.write(data + "\n" + message)
        self._lock.release()
