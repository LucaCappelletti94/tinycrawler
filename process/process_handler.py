from multiprocessing import Process
from abc import ABC
import queue

class process_handler:

    _processes = []

    def __init__(self, statistics):
        self._statistics = statistics

    def process(self, name, target):
        self._processes.append(Process(target=self._job_wrapper(name, target)))

    def _job_wrapper(self, name, target):
        def _job():
            self._statistics.set_process_running(name, True)
            while(True):
                try:
                    target()
                except queue.Empty:
                    break
            self._statistics.set_process_running(name, False)
        return _job

    def run(self):
        """Starts the parser"""
        for p in self._processes:
            p.start()

    def join(self):
        """Waits for the parser process to terminate"""
        for p in self._processes:
            p.join()