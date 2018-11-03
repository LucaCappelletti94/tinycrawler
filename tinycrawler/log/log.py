import logging
from multiprocessing import Lock


class Log:
    def __init__(self, directory):
        self._lock = Lock()
        self._path = "%s/error.log" % (directory)
        logging.basicConfig(filename=self._path,  level=logging.INFO)
        with open(self._path, 'w') as f:
            pass

    def _log(self, logger, message):
        self._lock.acquire()
        logger(message)
        self._lock.release()

    def log(self, message):
        """Log message with lock semaphore in info level."""
        self._log(logging.info, message)

    def error(self, message):
        """Log message with lock semaphore in error level."""
        self._log(logging.error, message)
