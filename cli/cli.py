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
        self._max_output = 0
        self._outputs = {}

    def _cli(self):
        self._statistics.set_start_time()
        self._stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        while True:
            time.sleep(0.1)
            self._clear()

            downloaded = self._statistics.get_downloaded()
            parsed = self._statistics.get_parsed()
            written = self._statistics.get_written()
            total = self._statistics.get_total()
            failed = self._statistics.get_failed()
            binary = self._statistics.get_binary_requests()
            total_downloaders = self._statistics.get_total_downloaders()
            processes_waiting_proxies =  self._statistics.get_processes_waiting_proxies()
            processes_waiting_urls =  self._statistics.get_processes_waiting_urls()

            self._print_fraction("Downloaded pages", downloaded, total)
            if downloaded != 0:
                self._print_fraction("Parsed pages", parsed, downloaded)
                self._print_fraction("Written pages", written, parsed)

            if failed != 0:
                self._print_fraction("Failed pages", failed, downloaded)
            if binary != 0:
                self._print_fraction("Binary requests", binary, downloaded)

            for code, number in self._statistics.get_error_codes().items():
                self._print_fraction("Error code %s"%code, number, downloaded)
            self._print_fraction("Free proxies", self._statistics.get_free_proxies(), self._statistics.get_total_proxies())

            if processes_waiting_proxies != 0:
                self._print_fraction("Downloaders waiting proxy", processes_waiting_proxies, total_downloaders)

            if processes_waiting_urls != 0:
                self._print_fraction("Downloaders waiting urls", processes_waiting_urls, total_downloaders)

            elaboration_speed = self._statistics.get_elaboration_speed()
            growth_speed = self._statistics.get_growth_speed()

            if elaboration_speed != 0:
                self._print_label("Elaboration speed", str(round(elaboration_speed, 2))+" url/s")

            if growth_speed != 0:
                self._print_label("Pool growth speed", str(round(growth_speed, 2))+" url/s")

            self._print_label("Elapsed time", self._statistics.get_elapsed_time())
            self._print_label("Estimated remaining time", self._statistics.get_remaining_time())

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
        self._print("-"*self._max_len, pos)

    def _print_label(self, label, value, pos=None):
        self._print("%s: §%s"%(label, value), pos)

    def _print(self, value, pos=None):
        if pos == None:
            pos = self._i

        self._max_len = max(self._max_len, len(value))

        self._outputs.update({
            pos: value
        })
        self._i+=1

    def _print_all(self):
        for k, v in self._outputs.items():
            if "§" in v:
                a, b = v.split("§")
                padding = " "*(self._max_len-len(v))
                v = a+padding+b
            self._stdscr.addstr(k, 0, v)

    def _clear(self):
        for i in range(self._i):
            self._stdscr.addstr(i, 0, " "*self._max_len)

        self._stdscr.refresh()
        self._i = 1
        self._max_len = 0
        self._outputs = {}

    def run(self):
        self._cli_process = Process(target=self._cli, name="cli")
        self._cli_process.start()

    def join(self):
        self._cli_process.join()
