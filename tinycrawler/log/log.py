import logging
from multiprocessing import Lock


class Log:
    def __init__(self, log_filename: str):
        self._lock = Lock()
        logging.basicConfig(filename=log_filename,  level=logging.INFO)

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
