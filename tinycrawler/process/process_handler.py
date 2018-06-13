import queue
import time
import traceback
from abc import ABC
from multiprocessing import Process


class process_handler:

    def __init__(self, statistics, logger):
        self._statistics = statistics
        self._logger = logger
        self._processes = []

    def process(self, objective, name, target):
        self._processes.append(
            Process(target=self._job_wrapper(objective, name, target), name=name))

    def _job_wrapper(self, objective, name, target):
        def _job():
            try:
                time.sleep(1)
                self._statistics.set_live_process(objective)
                while(True):
                    try:
                        target()
                    except queue.Empty:
                        self._logger.log(
                            "Process %s: has finished queue" % (name))
                        break
            except Exception as e:
                self._logger.log("Process %s: %s" %
                                 (name, traceback.format_exc()))
            self._statistics.set_dead_process(objective)
        return _job

    def run(self):
        """Starts the parser"""
        [p.start() for p in self._processes]

    def join(self):
        """Waits for the parser process to terminate"""
        for p in self._processes:
            p.join()
