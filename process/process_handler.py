from multiprocessing import Process
from abc import ABC
import queue
import time

class process_handler:

    def __init__(self, statistics, logger):
        self._statistics = statistics
        self._logger = logger
        self._processes = []

    def process(self, objective, name, target):
        self._processes.append(Process(target=self._job_wrapper(objective, name, target), name=name))

    def _job_wrapper(self, objective, name, target):
        def _job():
            try:
                time.sleep(1)
                self._statistics.set_live_process(objective)
                while(True):
                    try:
                        target()
                    except queue.Empty:
                        break
            except Exception as e:
                self._statistics.set_dead_process(objective)
                self._logger.log("Process %s: %s"%(name, e))
        return _job

    def run(self):
        """Starts the parser"""
        [p.start() for p in self._processes]

    def join(self):
        """Waits for the parser process to terminate"""
        for p in self._processes:
            p.join()