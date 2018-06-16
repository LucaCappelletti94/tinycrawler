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
        sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=40, cols=70))

    def _init_curses(self):
        self._stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()

    def _close_curses(self):
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def _cli_loop(self):
        cryouts = 0
        while True:
            time.sleep(0.1)
            if self._statistics.is_everything_dead():
                cryouts += 1
            if cryouts == self.CRYOUTS:
                break
            self._clear()

            info = self._statistics.get_informations()
            self._print_frame()
            for section, sub_dict in info.items():
                self._print(section.upper() + "@")
                self._print_frame()
                for label, value in sub_dict.items():
                    self._print_label(label, value)
                self._print_frame()

            self._print_all()

    def _cli(self):
        self._init_curses()
        try:
            self._cli_loop()
        except Exception as e:
            self._logger.error("cli: %s" % traceback.format_exc())
        except KeyboardInterrupt:
            pass
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
            self._stdscr.addstr(k, 0, v)

        self._stdscr.refresh()

    def _clear(self):
        for i in range(self._i):
            self._stdscr.addstr(i, 0, " " * self._max_len)

        self._stdscr.refresh()
        self._i = 1
        self._max_len = 0
        self._outputs = {}

    def run(self):
        self._cli_process = Process(target=self._cli, name="cli")
        self._cli_process.start()

    def join(self):
        self._cli_process.join()
