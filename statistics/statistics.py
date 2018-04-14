from multiprocessing import Lock
from .derivative import derivative
from datetime import datetime, timedelta
import time

class statistics:
    def __init__(self):
        self._lock = Lock()
        self._running_processes = {}
        self._parsed = 0
        self._parsed_graph = 0
        self._downloaded = 0
        self._total = 0
        self._failed = 0
        self._total_proxies = 0
        self._free_proxies = 0
        self._downloaded_bites = 0
        self._saved_bites = 0
        self._processes_waiting_proxies = 0
        self._processes_waiting_urls = 0
        self._total_downloaders = 0
        self._binary_requests = 0
        self._error_codes = {}
        self._start_time = time.time()
        self._estimate_update_timeout = 3
        self._last_estimate_update = 0
        self._bite = False

        self._elaboration_speed = derivative(1)
        self._pool_growth_speed = derivative(1)
        self._page_parsing_speed = derivative(1)
        self._graph_parsing_speed = derivative(1)

    def bite(self):
        self._bite = True

    def has_bitten(self):
        return self._bite

    def set_start_time(self):
        self._start_time = time.time()

    def set_total_downloaders(self, total):
        self._total_downloaders = total

    def add_downloaded(self, value):
        self._lock.acquire()
        self._downloaded += 1
        self._downloaded_bites += value
        self._lock.release()

    def add_parsed(self, value):
        self._lock.acquire()
        self._parsed += 1
        self._saved_bites += value
        self._lock.release()

    def add_parsed_graph(self):
        self._lock.acquire()
        self._parsed_graph += 1
        self._lock.release()

    def add_total(self, delta):
        self._lock.acquire()
        self._total += delta
        self._lock.release()

    def add_failed(self):
        self._lock.acquire()
        self._failed += 1
        self._lock.release()

    def add_binary_request(self):
        self._lock.acquire()
        self._binary_requests += 1
        self._lock.release()

    def add_error_code(self, code):
        self._lock.acquire()
        delta = 1
        if code in self._error_codes.keys():
            delta += self._error_codes[code]
        self._error_codes.update({
            code: delta
        })
        self._lock.release()

    def set_live_process(self, name):
        self._lock.acquire()
        delta = 1
        if name in self._running_processes.keys():
            delta += self._running_processes[name]
        self._running_processes.update({
            name: delta
        })
        self._lock.release()

    def set_dead_process(self, name):
        self._lock.acquire()
        delta = -1
        if name in self._running_processes.keys():
            delta += self._running_processes[name]
        self._running_processes.update({
            name: delta
        })
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

    def get_downloaded(self):
        return self._downloaded

    def get_parsed(self):
        return self._parsed

    def get_parsed_graph(self):
        return self._parsed_graph

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

    def get_binary_requests(self):
        return self._binary_requests

    def get_error_codes(self):
        return self._error_codes

    def get_running_processes(self):
        return self._running_processes

    def _format_value(self,response,value,pattern):
        if value > 0:
            if response != "":
                response+=", "
            response += pattern%value
        return response

    def _seconds_to_string(self, delta):

        if delta <= 1:
            return "now"

        d = datetime(1,1,1) + timedelta(seconds=delta)

        eta = ""
        if d.day-1>0:
            eta += "%sd"%(d.day-1)

        eta = self._format_value(eta,d.hour,  "%sh")
        eta = self._format_value(eta,d.minute, "%sm")
        eta = self._format_value(eta,d.second,"%ss")

        return eta

    def _get_remaining_time(self, delta, speed):
        if speed == 0:
            return "infinite"
        return self._seconds_to_string(delta/speed)

    def step_speeds(self):
        if time.time() - self._last_estimate_update > self._estimate_update_timeout:
            self._last_estimate_update = time.time()
            self._elaboration_speed.step(self._downloaded)
            self._pool_growth_speed.step(self._total)
            self._page_parsing_speed.step(self._parsed)
            self._graph_parsing_speed.step(self._parsed_graph)

    def get_remaining_elaboration_time(self):
        return self._get_remaining_time(
            self._pool_growth_speed.position() - self._elaboration_speed.position(),
            self._elaboration_speed.speed()
        )

    def get_remaining_page_parsing_time(self):
        return self._get_remaining_time(
            self._elaboration_speed.position() - self._page_parsing_speed.position(),
            self._page_parsing_speed.speed()
        )

    def get_remaining_graph_parsing_time(self):
        return self._get_remaining_time(
            self._elaboration_speed.position() - self._graph_parsing_speed.position(),
            self._graph_parsing_speed.speed()
        )

    def get_pool_growth_speed(self):
        return self._pool_growth_speed.speed()

    def get_elaboration_speed(self):
        return self._elaboration_speed.speed()

    def get_page_parsing_speed(self):
        return self._page_parsing_speed.speed()

    def get_graph_parsing_speed(self):
        return self._graph_parsing_speed.speed()

    def get_elapsed_time(self):
        return self._seconds_to_string(time.time()-self._start_time)

    def _bite_to_string(self, data):
        units = ["B", "KB", "MB", "GB", "TB"]

        response = "unable to estimate"

        for unit in units:
            if int(data) > 0:
                response = "%s %s"%(round(data, 2), unit)
            data /= 1024

        return response

    def get_downloaded_bites(self):
        return self._bite_to_string(self._downloaded_bites)

    def get_saved_bites(self):
        return self._bite_to_string(self._saved_bites)

    def get_saving_bites_speed(self):
        return self._bite_to_string(self._saved_bites/(time.time() - self._start_time)) + "/s"

    def get_download_bites_speed(self):
        return self._bite_to_string(self._downloaded_bites/(time.time() - self._start_time)) + "/s"


