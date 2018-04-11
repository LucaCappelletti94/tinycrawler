from multiprocessing import Lock
from datetime import datetime, timedelta
import time

class statistics:
    def __init__(self):
        self._lock = Lock()
        self._running_processes = {}
        self._done = 0
        self._total = 0
        self._failed = 0
        self._total_proxies = 0
        self._free_proxies = 0
        self._processes_waiting_proxies = 0
        self._processes_waiting_urls = 0
        self._total_downloaders = 0
        self._start_time = time.time()

    def set_start_time(self):
        self._start_time = time.time()

    def set_total_downloaders(self, total):
        self._total_downloaders = total

    def add_done(self):
        self._done += 1

    def add_total(self, delta):
        self._total += delta

    def add_failed(self):
        self._lock.acquire()
        self._failed += 1
        self._lock.release()

    def add_process_waiting_proxy(self):
        self._lock.acquire()
        self._processes_waiting_proxies += 1
        self._lock.release()

    def add_process_waiting_url(self):
        self._lock.acquire()
        self._processes_waiting_urls += 1
        self._lock.release()

    def remove_process_waiting_proxy(self):
        self._lock.acquire()
        self._processes_waiting_proxies -= 1
        self._remove_free_proxy()
        self._lock.release()

    def remove_process_waiting_url(self):
        self._lock.acquire()
        self._processes_waiting_urls -= 1
        self._lock.release()

    def set_total_proxies(self, total_proxies):
        self._total_proxies = total_proxies
        self._free_proxies = total_proxies

    def add_free_proxy(self):
        self._lock.acquire()
        self._free_proxies +=1
        self._lock.release()

    def _remove_free_proxy(self):
        self._free_proxies -=1

    def get_done(self):
        return self._done

    def get_total(self):
        return self._total

    def get_failed(self):
        return self._failed

    def get_free_proxies(self):
        return self._free_proxies

    def get_processes_waiting_urls(self):
        return self._processes_waiting_urls

    def get_processes_waiting_proxies(self):
        return self._processes_waiting_proxies

    def get_total_proxies(self):
        return self._total_proxies

    def get_total_downloaders(self):
        return self._total_downloaders

    def _format_value(self,response,value,pattern):
        if value > 0:
            if response != "":
                response+=", "
            response += pattern%value
        return response

    def _seconds_to_string(self, delta):

        if delta <= 0:
            return "now"

        d = datetime(1,1,1) + timedelta(seconds=delta)

        eta = ""
        if d.day-1>0:
            eta += "%sd"%(d.day-1)

        eta = self._format_value(eta,d.hour,  "%sh")
        eta = self._format_value(eta,d.minute, "%sm")
        eta = self._format_value(eta,d.second,"%ss")

        return eta

    def get_elapsed_time(self):
        return self._seconds_to_string(time.time()-self._start_time)