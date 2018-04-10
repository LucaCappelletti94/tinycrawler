import json
import requests
from multiprocessing import Pool, cpu_count, Queue
from tqdm import tqdm
import time
import os

class ProxiesQueue(Queue):

    _path = os.path.join(os.path.dirname(__file__), 'proxies.json')
    _cache_path = os.path.join(os.path.dirname(__file__), 'tested_proxies.json')
    _processes = cpu_count()*4
    _test_timeout = 10
    _proxy_timeout = 10

    def __init__(self, proxy_test_server, cache = True, cache_timeout = 100, https_only=True, remote=True):

        self.https_only = https_only
        self._server = proxy_test_server
        self._cache = cache
        self._cache_timeout = cache_timeout

        if remote:
            self._load()

        self.put({
            "local":True,
            "start":0
        })

        self._total_proxies = len(self._proxies)

    def _is_cache_enabled(self):
        return self._cache

    def _is_cached(self):
        return self._is_cache_enabled() and os.path.isfile(self._cache_path) and os.path.getmtime(self._cache_path) > time.time() - self._cache_timeout

    def _load(self):
        if self._is_cached():
            with open(self._cache_path, "r") as f:
                self._proxies = json.load(f)
        else:
            with open(self._path) as f:
                proxies_list = json.load(f)
            with Pool(self._processes) as p:
                self._proxies = list(filter(lambda x: x!=False, tqdm(p.imap(self._test_connection, proxies_list), total=len(proxies_list), desc="Testing proxies", leave=True)))
            if self._is_cache_enabled():
                with open(self._cache_path, "w") as f:
                    json.dump(self._proxies, f)

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

    def get(self, block = True, timeout = None):
        proxy = super().get(block = block, timeout = timeout)
        if proxy["start"]==0:
            timeout = 0
        else:
            timeout = max(0, self._proxy_timeout - (time.time()-proxy["start"]))
        proxy["start"] = time.time()
        return proxy, timeout
