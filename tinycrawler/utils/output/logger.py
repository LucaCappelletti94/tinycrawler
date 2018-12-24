"""Create a process-safe process object."""
import logging
import os
from multiprocessing import Lock


class Logger:
    """Create a process-safe process object."""

    def __init__(self, log_filename: str, level=logging.INFO, **kwargs):
        """Create a process-safe process object."""
        self._lock = Lock()
        os.makedirs(os.path.dirname(log_filename),  exist_ok=True)
        open(log_filename, 'w').close()
        logging.basicConfig(
            filename=log_filename,
            level=level
        )

    def _log(self, logger, message):
        with self._lock:
            logger(message)

    def info(self, message):
        """Log message with lock semaphore in info level."""
        self._log(logging.info, message)

    def warning(self, message):
        """Log message with lock semaphore in warning level."""
        self._log(logging.warning, message)

    def error(self, message):
        """Log message with lock semaphore in error level."""
        self._log(logging.error, message)

    def critical(self, message):
        """Log message with lock semaphore in critical level."""
        self._log(logging.critical, message)
