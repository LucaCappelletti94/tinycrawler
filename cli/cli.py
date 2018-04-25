from __future__ import division
import sys
import curses
import time
from datetime import datetime, timedelta
from multiprocessing import Process
import traceback
import json

class cli:
    def __init__(self, statistics, logger):
        self._statistics = statistics
        self._logger = logger
        self._i=0
        self._max_len = 0
        self._outputs = {}

    def _cli(self):
        self._statistics.set_start_time()
        self._stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        try:
            while True:
                time.sleep(0.1)
                if self._statistics.is_done():
                    break
                self._clear()
                self._statistics.step_speeds()

                downloaded = self._statistics.get_downloaded()
                parsed = self._statistics.get_parsed()
                discarted = self._statistics.get_discarted()
                parsed_graph = self._statistics.get_parsed_graph()
                total = self._statistics.get_total()
                failed = self._statistics.get_failed()
                binary = self._statistics.get_binary_requests()
                total_downloaders = self._statistics.get_total_downloaders()
                processes_waiting_proxies =  self._statistics.get_processes_waiting_proxies()
                processes_waiting_urls =  self._statistics.get_processes_waiting_urls()

                total_downloaded = downloaded+failed+binary+self._statistics.get_total_error_pages()

                self._print_fraction("Downloaded pages", total_downloaded, total)
                if downloaded != 0:
                    self._print_fraction("Parsed pages", parsed, downloaded)
                    self._print_fraction("Parsed page graphs", parsed_graph, downloaded)
                    if discarted*parsed:
                        self._print_fraction("Discarted pages", discarted, parsed)

                if failed != 0:
                    self._print_fraction("Failed pages", failed, total_downloaded)
                if binary != 0:
                    self._print_fraction("Binary requests", binary, total_downloaded)

                error_codes = self._statistics.get_error_codes().items()

                if len(error_codes):
                    self._print_frame()
                    for code, number in error_codes:
                        self._print_fraction("Error code %s"%code, number, downloaded)

                self._print_fraction("Free proxies", self._statistics.get_free_proxies(), self._statistics.get_total_proxies())

                self._print_frame()

                self._print_fraction("Downloaders waiting proxy", processes_waiting_proxies, total_downloaders)

                self._print_fraction("Downloaders waiting urls", processes_waiting_urls, total_downloaders)

                self._print_speeds()

                self._print_data_size()

                self._print_times()

                processes = self._statistics.get_running_processes().items()

                if len(processes)>0:
                    self._print_frame()
                    for name, number in processes:
                        self._print_label("Process %s"%name, number)

                self._print_all()

        except Exception as e:
            self._logger.log("cli: %s"%traceback.format_exc())

        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def _print_data_size(self):
        self._print_frame()
        self._print_label("Downloaded data", self._statistics.get_downloaded_bites())
        self._print_label("Saved data", self._statistics.get_saved_bites())
        self._print_label("Data saving speed", self._statistics.get_saving_bites_speed())
        self._print_label("Data download speed", self._statistics.get_download_bites_speed())

    def _print_times(self):
        self._print_frame()
        self._print_label("Elapsed time", self._statistics.get_elapsed_time())
        self._print_label("Elaboration remaining time", self._statistics.get_remaining_elaboration_time())
        self._print_label("Page parsing remaining time", self._statistics.get_remaining_page_parsing_time())
        self._print_label("Graph parsing remaining time", self._statistics.get_remaining_graph_parsing_time())

    def _print_speeds(self):
        elaboration_speed = self._statistics.get_elaboration_speed()
        growth_speed = self._statistics.get_pool_growth_speed()
        page_parsing_speed = self._statistics.get_page_parsing_speed()
        graph_parsing_speed = self._statistics.get_graph_parsing_speed()

        if elaboration_speed + growth_speed + page_parsing_speed + graph_parsing_speed != 0:
            self._print_frame()

        self._print_speed("Elaboration", elaboration_speed)
        self._print_speed("Pool growth", growth_speed)
        self._print_speed("Page parsing", page_parsing_speed)
        self._print_speed("Graph parsing", graph_parsing_speed)

    def _print_speed(self, label, value):
        if value != 0:
            self._print_label("%s speed"%label, "%s url/s"%round(value, 2))

    def _print_fraction(self, label, v1, v2):
        if v2 != 0:
            perc = str(round(v1/v2*100, 1))+"%"

            self._print_label(label, "%s/%s %s"%(
                v1,
                v2,
                perc
            ))

    def _print_frame(self, pos=None):
        self._print("$$$", pos)

    def _print_label(self, label, value, pos=None):
        self._print("%s: § %s"%(label, value), pos)

    def _print(self, value, pos=None):
        if pos == None:
            pos = self._i

        value = "| "+value+" |"

        self._max_len = max(self._max_len, len(value))

        self._outputs.update({
            pos: value
        })
        self._i+=1

    def _print_all(self):
        self._print_frame(0)
        self._print_frame(self._i-1)
        for k, v in self._outputs.items():
            if "| $$$ |" == v:
                v = "| "+("-"*(self._max_len-5))+" |"
            elif "§" in v:
                a, b = v.split("§")
                padding = " "*(self._max_len-len(v))
                v = a+padding+b
            self._stdscr.addstr(k, 0, v)

        self._stdscr.refresh()

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
