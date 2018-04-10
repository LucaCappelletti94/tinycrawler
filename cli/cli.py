import sys
import curses
import time
from datetime import datetime, timedelta
from multiprocessing import Process

class cli:
    def __init__(self, statistics):
        self._statistics = statistics

    def _cli(self):
        self._stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        try:
            while True:
                time.sleep(1)

                self._stdscr.addstr(0, 0, "%s/%s"%(
                    self._statistics.get_done(),
                    self._statistics.get_total()
                ))

                self._stdscr.refresh()
        except Exception as e:
            pass

        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def run(self):
        self._cli_process = Process(target=self._cli)
        self._cli_process.start()

    def join(self):
        self._cli_process.join()