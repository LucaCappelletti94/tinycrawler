import json
import requests
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import time
import os
import queue

class proxiesqueue(queue.Queue):

    _proxy_timeout = 10

    def __init__(self):
        super().__init__()

        self.put({
            "local":True,
            "start":0
        })

    def get(self, block = True, timeout = None):
        proxy = super().get(block = block, timeout = timeout)
        if proxy["start"]==0:
            timeout = 0
        else:
            timeout = max(0, self._proxy_timeout - (time.time()-proxy["start"]))
        proxy["start"] = time.time()
        return proxy, timeout


class proxiesloader:
    _path = os.path.join(os.path.dirname(__file__), 'proxies.json')
    _cache_path = os.path.join(os.path.dirname(__file__), 'tested_proxies.json')
    _processes = cpu_count()*4
    _test_timeout = 10

    def __init__(self, proxy_test_server, https_only=True):
        super().__init__()
        self.https_only = https_only
        self._server = proxy_test_server


    def load(self, proxy_queue):
        with open(self._path) as f:
            proxies_list = json.load(f)
        with Pool(self._processes) as p:
            [proxy_queue.put(x) for x in list(filter(lambda x: x!=False, tqdm(p.imap(self._test_connection, proxies_list), total=len(proxies_list), desc="Testing proxies", leave=True)))]
        proxy_queue.put({
            "local":True,
            "start":0
        })

    def _test_connection(self, proxy):
        if self.https_only and not (proxy["support"]["https"] or proxy["support"]["socks4"] or proxy["support"]["socks5"]):
            pass
        else:
            try:
                proxies = self._proxy_to_urls(proxy)
                requests.get(self._server, proxies = proxies, timeout=self._test_timeout)
                return proxies
            except Exception as e:
                pass
        return False

    def _proxy_to_urls(self, proxy_info):
        url = "://%s:%s"%(proxy_info["ip"], proxy_info["port"])
        proxy = {
            "local":False,
            "urls":{},
            "start":0
        }

        if proxy_info["support"]["http"]:
            proxy["urls"].update({
                "http": "http%s"%url
            })

        if proxy_info["support"]["https"]:
            proxy["urls"].update({
                "https": "https%s"%url
            })

        if proxy_info["support"]["socks4"]:
            proxy["urls"].update({
                "https": "socks4%s"%url,
                "http": "socks4%s"%url,
            })

        if proxy_info["support"]["socks5"]:
            proxy["urls"].update({
                "https": "socks5%s"%url,
                "http": "socks5%s"%url,
            })

        return proxy