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
        self._outputs = {}
        self._estimate_update_timeout = 10
        self._last_estimate_update = 0

    def _cli(self):
        self._statistics.set_start_time()
        self._stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        while True:
            time.sleep(0.1)
            self._clear()

            done = self._statistics.get_done()
            total = self._statistics.get_total()
            failed = self._statistics.get_failed()
            binary = self._statistics.get_binary_requests()
            total_downloaders = self._statistics.get_total_downloaders()

            self._print_fraction("Downloaded pages", done, total)
            if failed != 0:
                self._print_fraction("Failed pages", failed, done)
            if binary != 0:
                self._print_fraction("Binary requests", binary, done)

            for code, number in self._statistics.get_error_codes().items():
                self._print_fraction("Error code %s"%code, number, done)
            self._print_fraction("Free proxies", self._statistics.get_free_proxies(), self._statistics.get_total_proxies())
            self._print_fraction("Downloaders waiting proxy", self._statistics.get_processes_waiting_proxies(), total_downloaders)
            self._print_fraction("Downloaders waiting urls", self._statistics.get_processes_waiting_urls(), total_downloaders)

            elaboration_speed = self._statistics.get_elaboration_speed()
            growth_speed = self._statistics.get_growth_speed()

            if elaboration_speed != 0:
                self._print_label("Elaboration speed", str(round(elaboration_speed, 2))+" url/s")

            if growth_speed != 0:
                self._print_label("Pool growth speed", str(round(growth_speed, 2))+" url/s")

            if time.time() - self._last_estimate_update > self._estimate_update_timeout:
                self._elapsed_time = self._statistics.get_remaining_time()
                self._last_estimate_update = time.time()

            self._print_label("Elapsed time", self._statistics.get_elapsed_time())
            self._print_label("Estimated remaining time", self._elapsed_time)

            self._print_frame(0)
            self._print_frame(self._i-1)

            self._print_all()

            self._stdscr.refresh()

        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def _print_fraction(self, label, v1, v2):
        if v2 != 0:
            perc = str(round(v1/v2*100, 1))+"%"

            self._print_label(label, "%s/%s %s"%(
                v1,
                v2,
                perc
            ))

    def _print_frame(self, pos):
        self._print("-"*max(self._outputs_max_lenghts.values()), pos)

    def _print_label(self, label, value, pos=None):
        self._print("%s: §%s"%(label, value), pos)

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

    def _clear(self):
        if len(self._outputs_max_lenghts.values()) > 0:
            max_len = max(self._outputs_max_lenghts.values())
        max_len = 0
        for i in range(self._i):
            self._stdscr.addstr(i, 0, " "*max_len)
        self._stdscr.refresh()
        self._reset_cursor()

    def _reset_cursor(self):
        self._i = 1

    def run(self):
        self._cli_process = Process(target=self._cli, name="cli")
        self._cli_process.start()

    def join(self):
        self._cli_process.join()
