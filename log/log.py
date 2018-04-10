import logging
from multiprocessing import Lock

class log:
  def __init__(self, directory):
    self._lock = Lock()
    self._path = "%s/error.log"%(directory)
    logging.basicConfig(filename=self._path,level=logging.ERROR)
    with open(self._path, 'w'):
        pass

  def log(self, message):
    self._lock.acquire()
    logging.error(message)
    self._lock.release()

  def exception(self, e):
    self._lock.acquire()
    logging.exception(e, exc_info=True)
    self._lock.release()