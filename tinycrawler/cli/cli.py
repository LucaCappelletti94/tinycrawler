import curses
import time
from multiprocessing import Process, Event

from ..__version__ import __version__


class Cli:
    WINDOW_SIZE = 100
    PADDING = 8

    def __init__(self, statistics, logger, close_signal: Event):
        self._statistics = statistics
        self._logger = logger
        self._i = 0
        self._max_len = 0
        self._close_signal = close_signal
        self._outputs = {}

    def _init_curses(self):
        curses.initscr()
        self._window = curses.newwin(self.WINDOW_SIZE, self.WINDOW_SIZE, 0, 0)
        curses.noecho()

    def _close_curses(self):
        curses.echo()
        curses.endwin()

    def _print_info(self):
        self._print_frame()
        self._print("TINYCRAWLER {version}@".format(version=__version__))
        self._print_frame()
        sorted_sections = sorted(self._statistics.keys(), key=str.lower)
        for section in sorted_sections:
            self._print(section.upper() + "@")
            self._print_frame()
            sub_dict = self._statistics.get(section)
            sorted_keys = sorted(sub_dict.keys(), key=str.lower)
            for label in sorted_keys:
                self._print_label(label.capitalize(), sub_dict[label])
            self._print_frame()

    def _cli_loop(self):
        while True:
            time.sleep(0.2)
            if self._close_signal.is_set():
                break
            self._clear()

            self._print_info()

            self._print_all()

    def _cli(self):
        self._init_curses()
        try:
            self._cli_loop()
            self._close_curses()
        except KeyboardInterrupt:
            self._close_curses()
            self._logger.error("Shutting down crawler.")
            print("Shutting down crawler.")

    def _print_frame(self, pos=None):
        self._print("$$$", pos)

    def _print_label(self, label, value, pos=None):
        self._print("{label}@{value}".format(label=label, value=value)[:
                                                                       self.WINDOW_SIZE - self.PADDING*2], pos)

    def _print(self, value, pos=None):
        if pos is None:
            pos = self._i

        self._max_len = max(self._max_len, len(value))

        self._outputs.update({
            pos: value
        })
        self._i += 1

    def _print_all(self):
        max_len = self._max_len + self.PADDING
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
        for i in range(self.WINDOW_SIZE):
            self._window.addstr(i, 0, " " * (self.WINDOW_SIZE-1))

        self._window.refresh()
        self._i = 1
        self._max_len = 0
        self._outputs = {}

    def run(self):
        self._cli_process = Process(target=self._cli, name="cli")
        self._cli_process.start()

    def join(self):
        self._cli_process.join()
