from multiprocessing import Lock

class statistics:
    def __init__(self):
        self._lock = Lock()
        self._running_processes = {}
        self._done = 0
        self._total = 0
        self._failed = 0

    def set_process_running(self, name, status):
        self._lock.acquire()
        self._running_processes.update({
            name: status
        })
        self._lock.release()

    def add_done(self):
        self._done += 1

    def add_total(self, delta):
        self._total += delta

    def add_failed(self):
        self._lock.acquire()
        self._failed += 1
        self._lock.release()

    def get_done(self):
        return self._done

    def get_total(self):
        return self._total

    def get_failed(self):
        return self._failed

    def get_running_processes(self):
        return self._running_processes