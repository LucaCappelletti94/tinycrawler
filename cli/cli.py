from __future__ import division
import sys
import curses
import time
from datetime import datetime, timedelta
from multiprocessing import Process

class cli:
    def __init__(self, statistics):
        self._statistics = statistics
        self._i=0
        self._outputs_max_lenghts = {}
        self._speeds = []
        self._old_done = 0

    def _cli(self):
        self._stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        while True:
            time.sleep(1)
            self._reset_cursor()

            self._print("Downloaded pages: %s/%s"%(
                self._statistics.get_done(),
                self._statistics.get_total()
            ), self._i)

            self._print("Failed pages: %s/%s"%(
                self._statistics.get_failed(),
                self._statistics.get_done()
            ), self._i)

            self._speeds.append(self._statistics.get_done()-self._old_done)
            self._speeds = self._speeds[-1000:]
            self._old_done = self._statistics.get_done()

            self._print("Average speed: %s it/s"%(
                round(sum(self._speeds) / len(self._speeds),2)
            ), self._i)

            self._print_frame(0)
            self._print_frame(self._i-1)

            self._stdscr.refresh()

        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def _reset_cursor(self):
        self._i = 1

    def _print_frame(self, pos):
        self._print("-"*max(self._outputs_max_lenghts.values()), pos)

    def _print(self, value, pos):
        if pos in self._outputs_max_lenghts.keys():
            old_max = self._outputs_max_lenghts[pos]
        else:
            old_max = 0
        self._outputs_max_lenghts.update({
            pos: max(old_max, len(value))
        })

        self._stdscr.addstr(pos, 0, value)
        self._i+=1

    def run(self):
        self._cli_process = Process(target=self._cli)
        self._cli_process.start()

    def join(self):
        self._cli_process.join()