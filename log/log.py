import os
import logging

class Log:
  def __init__(self, directory):
    self._path = "%s/error.log"%(directory)
    if os.path.isfile(self._path):
        with open(self._path, 'w'):
            pass
    logging.basicConfig(filename=self._path,level=logging.ERROR)

  def log(self, message=""):
    logging.error(message)

  def exception(self, e):
    self.log("="*100)
    logging.exception(e)
