from multiprocessing import Process
from abc import ABC
import queue

class process_handler:

    _processes = []

    def __init__(self, statistics, logger):
        self._statistics = statistics
        self._logger = logger

    def process(self, name, target):
        self._processes.append(Process(target=self._job_wrapper(name, target), name=name))

    def _job_wrapper(self, name, target):
        def _job():
            try:
                self._statistics.set_process_running(name, True)
                while(True):
                    try:
                        target()
                        break
                    except queue.Empty:
                        break
                self._statistics.set_process_running(name, False)
            except Exception as e:
                self._logger.exception(e)

        return _job

    def run(self):
        """Starts the parser"""
        try:
            for p in self._processes:
                p.start()
        except Exception as e:
            self._logger.exception(e)

    def join(self):
        """Waits for the parser process to terminate"""
        for p in self._processes:
            p.join()