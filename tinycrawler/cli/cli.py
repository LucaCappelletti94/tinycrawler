from __future__ import division

import curses
import json
import sys
import time
import traceback
from datetime import datetime, timedelta
from multiprocessing import Process

from ..__version__ import __version__


class Cli:
    CRYOUTS = 2

    def __init__(self, statistics, logger):
        self._statistics = statistics
        self._logger = logger
        self._i = 0
        self._max_len = 0
        self._outputs = {}

    def _init_curses(self):
        curses.initscr()
        self._window = curses.newwin(70, 70, 0, 0)
        curses.noecho()

    def _close_curses(self):
        curses.echo()
        curses.endwin()

    def _print_informations(self):
        informations = self._statistics.get_informations()
        self._print_frame()
        self._print("TINYCRAWLER %s@" % __version__)
        self._print_frame()
        sorted_sections = sorted(informations.keys(), key=str.lower)
        for section in sorted_sections:
            self._print(section.upper() + "@")
            self._print_frame()
            sub_dict = informations[section]
            sorted_keys = sorted(sub_dict.keys(), key=str.lower)
            for label in sorted_keys:
                self._print_label(label.capitalize(), sub_dict[label])
            self._print_frame()

    def _cli_loop(self):
        cryouts = 0
        while True:
            time.sleep(0.1)
            if self._statistics.is_everything_dead():
                cryouts += 1
            else:
                cryouts = 0
            if cryouts == self.CRYOUTS:
                break
            try:
                self._clear()
            except curses.error:
                pass

            self._print_informations()

            try:
                self._print_all()
            except curses.error:
                pass

    def _cli(self):
        self._init_curses()
        try:
            self._cli_loop()
            self._close_curses()
        except Exception as e:
            self._close_curses()
            self._logger.error("cli: %s" % traceback.format_exc())
            print("Cli has crashed, checkout log for more informations.")
        except KeyboardInterrupt:
            self._close_curses()
            print("Shutting down crawler.")

    def _print_frame(self, pos=None):
        self._print("$$$", pos)

    def _print_label(self, label, value, pos=None):
        self._print("%s@%s" % (label, value), pos)

    def _print(self, value, pos=None):
        if pos is None:
            pos = self._i

        self._max_len = max(self._max_len, len(value))

        self._outputs.update({
            pos: value
        })
        self._i += 1

    def _print_all(self):
        padding = 8
        max_len = self._max_len + padding
        for k, v in self._outputs.items():
            self._window.addstr(k, 0, "|", curses.A_DIM)
            self._window.addstr(k, max_len, "|", curses.A_DIM)
            if "$$$" == v:
                v = ("-" * (max_len - 1))
                self._window.addstr(k, 1, v, curses.A_DIM)
            elif "@" in v:
                a, b = v.split("@")
                if len(b) == 0:
                    self._window.addstr(k, 2, a, curses.A_BOLD)
                else:
                    b = " " * (max_len - len(b) - 3) + b + " "
                    self._window.addstr(k, 2, b)
                    self._window.addstr(k, 2, a, curses.A_UNDERLINE)
                    self._window.addstr(k, 2 + len(a), ":")

        self._window.refresh()

    def _clear(self):
        for i in range(self._i):
            self._window.addstr(i, 0, " " * (self._max_len + 8 + 4))

        self._window.refresh()
        self._i = 1
        self._max_len = 0
        self._outputs = {}

    def run(self):
        self._cli_process = Process(target=self._cli, name="cli")
        self._cli_process.start()

    def join(self):
        self._cli_process.join()
