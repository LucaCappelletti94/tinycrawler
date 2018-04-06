import sys
import curses
import time
from datetime import datetime, timedelta

class Bar:
    _parameters = {}
    _outputs = [
        "Currently downloading from {domain}",
        "Active daemons: {active_daemons}/{total_daemons}",
        "Free proxies: {free_proxies}/{total_proxies}",
        "Downloaded pages: {parsed_urls}/{total_urls}",
        "Updating cache in: {cache_update_time}",
        "Estimated speed: {speed}{speed_unit}",
        "Expected remaining time: {remaining_time}",
        "Elapsed time: {elapsed_time}"
    ]
    _outputs_lenghts = [0]*len(_outputs)
    _estimated_step_time = 0
    _old_parsed_urls = 0
    _parsed_urls = 0
    _active_daemons = 0

    def __init__(self, domain, total_daemons, total_proxies):
        self._active_daemons = total_daemons
        self._parameters.update({
            "domain":domain,
            "total_proxies":total_proxies,
            "total_daemons":total_daemons
        })

    def _format_value(self,response,value,pattern):
        if value > 0:
            if response != "":
                response+=", "
            response += pattern%value
        return response

    def _seconds_delta(self):
        return (self._total_urls-self._parsed_urls)*self._estimated_step_time

    def _seconds_to_string(self, delta):

        d = datetime(1,1,1) + timedelta(seconds=delta)

        eta = ""
        if d.day-1>0:
            eta += "%sd"%(d.day-1)

        eta = self._format_value(eta,d.hour,  "%sh")
        eta = self._format_value(eta,d.minute, "%sm")
        eta = self._format_value(eta,d.second,"%ss")

        return eta

    def _update_estimated(self, old_estimate, delta):
        if old_estimate == 0:
            return delta
        else:
            return old_estimate*0.99 + 0.01*(delta)

    def _estimate_speed(self):
        if self._estimated_step_time <1 and self._estimated_step_time != 0:
            return round(1/self._estimated_step_time, 2), "it/s"
        else:
            return round(self._estimated_step_time, 2), "s/it"


    def _update_parameters(self):
        self._estimated_step_time = self._update_estimated(self._estimated_step_time, time.time()-self._start)

        speed, unit = self._estimate_speed()

        self._parameters.update({
            "speed":speed,
            "speed_unit":unit,
            "remaining_time":self._seconds_to_string(self._seconds_delta()),
            "elapsed_time": self._seconds_to_string(time.time()-self._start_time),
        })

        self._start = time.time()

    def _update_bar(self):
        for i, l in enumerate(self._outputs_lenghts):
            self._stdscr.addstr(i+1, 0, " "*l)
        self._stdscr.refresh()

        for i, output in enumerate(self._outputs):
            out = output.format(**self._parameters)
            self._outputs_lenghts[i] = max(len(out), self._outputs_lenghts[i])
            self._stdscr.addstr(i+1, 0, out)
        self._stdscr.addstr(0, 0, "-"*max(self._outputs_lenghts))
        self._stdscr.addstr(len(self._outputs)+1, 0, "-"*max(self._outputs_lenghts))
        self._stdscr.refresh()

    def start(self):
        self._stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self._start = time.time()
        self._start_time = time.time()

    def set_dead_daemon(self):
        self._active_daemons -= 1

    def finalize(self):
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def update(self, free_proxies, parsed_urls, total_urls, cache_update_time):
        self._old_parsed_urls = self._parsed_urls
        self._parsed_urls = parsed_urls
        self._total_urls = total_urls
        if cache_update_time == False:
            cache_update_string = "cache is disabled"
        else:
            cache_update_string = self._seconds_to_string(cache_update_time)

        self._parameters.update({
            "free_proxies":free_proxies,
            "parsed_urls":parsed_urls,
            "total_urls":total_urls,
            "active_daemons":self._active_daemons,
            "cache_update_time":cache_update_string
        })
        self._update_parameters()
        self._update_bar()


