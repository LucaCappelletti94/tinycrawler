from multiprocessing import Process
from abc import ABC
import queue
import time

class process_handler:

    def __init__(self, statistics, logger):
        self._statistics = statistics
        self._logger = logger
        self._processes = []

    def process(self, name, target):
        self._processes.append(Process(target=self._job_wrapper(name, target), name=name))

    def _job_wrapper(self, name, target):
        def _job():
            time.sleep(10)
            try:
                self._statistics.set_process_running(name, True)
                while(True):
                    try:
                        target()
                    except queue.Empty:
                        break
                self._statistics.set_process_running(name, False)
            except Exception as e:
                self._logger.log("Exception from process %s"%name)
                self._logger.exception(e)

        return _job

    def run(self):
        """Starts the parser"""
        [p.start() for p in self._processes]

    def join(self):
        """Waits for the parser process to terminate"""
        for p in self._processes:
            p.join()