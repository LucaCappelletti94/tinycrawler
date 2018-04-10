from multiprocessing import Lock

def statistics:
    def __init__(self):
        self._lock = Lock()
        self._running_processes = {}
        self._done = 0
        self._total = 0

    def set_process_running(self, name, status):
        self._lock.acquire()
        self._running_processes.update({
            name: status
        })
        self._lock.release()

    def set_done(self, done):
        self._done = done

    def set_total(self, total):
        self._total = total

    def get_done(self):
        return self._done

    def get_total(self):
        return self._total

    def get_running_processes(self):
        return self._running_processes