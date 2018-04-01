import sys
import curses
import time
from datetime import datetime, timedelta

class Bar:
    _parameters = {}
    _outputs = [
        "Currently downloading from {domain}",
        "Used daemons: {total_daemons}",
        "Free proxies: {free_proxies}/{total_proxies}",
        "Downloaded pages: {parsed_urls}/{total_urls}",
        "Updating cache in: {cache_update_time}",
        "Estimated speed: {speed}{speed_unit}",
        "Expected remaining time: {remaining_time}"
    ]
    _estimated_step_time = 0
    _estimated_step_units = 0
    _old_parsed_urls = 0
    _parsed_urls = 0

    def __init__(self, domain, total_daemons, total_proxies):
        self._start = 0
        self._stdscr = curses.initscr()
        self._parameters.update({
            "domain":domain,
            "total_proxies":total_proxies,
            "total_daemons":total_daemons
        })
        curses.noecho()
        curses.cbreak()

    def _format_value(self,response,value,pattern):
        if value > 0:
            if response != "":
                response+=", "
            response += pattern%value
        return response

    def _seconds_delta(self):
        return (self._total_urls-self._parsed_urls)/self._estimated_step_time*self._estimated_step_time

    def _estimate_remaining_time(self):

        d = datetime(1,1,1) + timedelta(seconds=self._seconds_delta())

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
            return old_estimate*0.999 + 0.001*(delta)

    def _estimate_speed(self):
        if self._estimated_step_time <1 and self._estimated_step_time != 0:
            return round(1/self._estimated_step_time, 2), "it/s"
        else:
            return round(self._estimated_step_time, 2), "s/it"


    def _update_parameters(self):
        self._estimated_step_time = self._update_estimated(self._estimated_step_time, time.time()-self._start)
        self._estimated_step_units = self._update_estimated(self._estimated_step_units, self._parsed_urls - self._old_parsed_urls)

        speed, unit = self._estimate_speed()

        self._parameters.update({
            "speed":speed,
            "speed_unit":unit,
            "remaining_time":self._estimate_remaining_time()
        })

        self._start = time.time()

    def _update_bar(self):
        for i, output in enumerate(self._outputs):
            self._stdscr.addstr(i, 0, output.format(**self._parameters))
        self._stdscr.refresh()

    def finalize(self):
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def update(self, free_proxies, parsed_urls, total_urls, cache_update_time):
        if self._start == 0:
            self._start = time.time()

        self._old_parsed_urls = self._parsed_urls
        self._parsed_urls = parsed_urls
        self._total_urls = total_urls
        if cache_update_time == False:
            cache_update_time = "cache is disabled"
        self._parameters.update({
            "free_proxies":free_proxies,
            "parsed_urls":parsed_urls,
            "total_urls":total_urls,
            "cache_update_time":cache_update_time
        })
        self._update_parameters()
        self._update_bar()


