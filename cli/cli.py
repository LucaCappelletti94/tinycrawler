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
        self._growing_speeds = []
        self._outputs = {}
        self._old_done = 0
        self._old_total = 0

    def _cli(self):
        time.sleep(1)
        self._statistics.set_start_time()
        self._stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        while True:
            time.sleep(1)

            self._clear()

            done = self._statistics.get_done()
            total = self._statistics.get_total()
            failed = self._statistics.get_failed()

            self._print_fraction("Downloaded pages", done, total)
            self._print_fraction("Failed pages", failed, done)
            self._print_fraction("Free proxies", self._statistics.get_free_proxies(), self._statistics.get_total_proxies())
            self._print_fraction("Downloaders waiting proxy", self._statistics.get_processes_waiting_proxies(), self._statistics.get_total_downloaders())
            self._print_fraction("Downloaders waiting urls", self._statistics.get_processes_waiting_urls(), self._statistics.get_total_downloaders())
            self._print_speed()
            self._print_growing_speed()
            self._print("Elapsed time: §%s"% self._statistics.get_elapsed_time())

            self._print_frame(0)
            self._print_frame(self._i-1)

            self._print_all()

            self._stdscr.refresh()

        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def _print_fraction(self, label, v1, v2):
        if v2 == 0:
            perc = "NaN"
        else:
            perc = str(round(v1/v2*100, 1))+"%"

        self._print("%s: §%s/%s %s"%(
            label,
            v1,
            v2,
            perc
        ))

    def _clear(self):
        for k, v in self._outputs_max_lenghts.items():
            self._stdscr.addstr(k, 0, " "*v)
        self._stdscr.refresh()
        self._reset_cursor()

    def _print_speed(self):
        done = self._statistics.get_done()
        self._speeds.append(done-self._old_done)
        self._speeds = self._speeds[-1000:]
        self._old_done = done

        self._print("Average speed: §%s it/s"%(
            round(sum(self._speeds) / len(self._speeds),2)
        ))

    def _print_growing_speed(self):
        total = self._statistics.get_total()
        self._growing_speeds.append(total-self._old_total)
        self._growing_speeds = self._growing_speeds[-1000:]
        self._old_total = total

        self._print("Growing speed: §%s url/s"%(
            round(sum(self._growing_speeds) / len(self._growing_speeds),2)
        ))

    def _reset_cursor(self):
        self._i = 1

    def _print_frame(self, pos):
        self._print("-"*max(self._outputs_max_lenghts.values()), pos)

    def _print(self, value, pos=None):
        if pos == None:
            pos = self._i
        if pos in self._outputs_max_lenghts.keys():
            old_max = self._outputs_max_lenghts[pos]
        else:
            old_max = 0
        self._outputs_max_lenghts.update({
            pos: max(old_max, len(value))
        })

        self._outputs.update({
            pos: value
        })
        self._i+=1

    def _print_all(self):
        max_len = max(self._outputs_max_lenghts.values())
        for k, v in self._outputs.items():
            if "§" in v:
                a, b = v.split("§")
                padding = " "*(max_len-len(v))
                v = a+padding+b
            self._stdscr.addstr(k, 0, v)

    def run(self):
        self._cli_process = Process(target=self._cli, name="cli")
        self._cli_process.start()

    def join(self):
        self._cli_process.join()
