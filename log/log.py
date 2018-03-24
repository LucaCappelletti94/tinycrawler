import logging

class Log:
  def __init__(self, directory):
    self._path = "%s.log"%(directory)
    if os.path.isfile(self._logPath):
        with open(self.path, 'w'):
            pass
    logging.basicConfig(filename=self.path,level=logging.ERROR)

  def log(self, message=""):
    logging.error(message)

  def exception(self, message=""):
    logging.exception(message)