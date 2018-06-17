from __future__ import division

import curses
import json
import sys
import time
import traceback
from datetime import datetime, timedelta
from multiprocessing import Process


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
        self._window = curses.newwin(60, 60, 0, 0)
        curses.noecho()
        curses.cbreak()

    def _close_curses(self):
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def _print_informations(self):
        informations = self._statistics.get_informations()
        self._print_frame()
        for section, sub_dict in informations.items():
            self._print(section.upper() + "@")
            self._print_frame()
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
            self._clear()

            self._print_informations()

            self._print_all()

    def _cli(self):
        self._init_curses()
        try:
            self._cli_loop()
            self._close_curses()
        except Exception as e:
            self._close_curses()
            self._logger.error("cli: %s" % traceback.format_exc())
        except KeyboardInterrupt:
            self._close_curses()

    def _print_fraction(self, label, v1, v2):
        if v2 != 0:
            perc = str(round(v1 / v2 * 100, 1)) + "%"

            self._print_label(label, "%s/%s %s" % (
                v1,
                v2,
                perc
            ))

    def _print_frame(self, pos=None):
        self._print("$$$", pos)

    def _print_label(self, label, value, pos=None):
        self._print("%s: @ %s" % (label, value), pos)

    def _print(self, value, pos=None):
        if pos is None:
            pos = self._i

        value = "| " + value + " |"

        self._max_len = max(self._max_len, len(value))

        self._outputs.update({
            pos: value
        })
        self._i += 1

    def _print_all(self):
        for k, v in self._outputs.items():
            if "| $$$ |" == v:
                v = "| " + ("-" * (self._max_len - 5)) + " |"
            elif "@" in v:
                a, b = v.split("@")
                padding = " " * (self._max_len - len(v))
                v = a + padding + b
            self._window.addstr(k, 0, v)

        self._window.refresh()

    def _clear(self):
        for i in range(self._i):
            self._window.addstr(i, 0, " " * self._max_len)

        self._window.refresh()
        self._i = 1
        self._max_len = 0
        self._outputs = {}

    def run(self):
        self._cli_process = Process(target=self._cli, name="cli")
        self._cli_process.start()

    def join(self):
        self._cli_process.join()
