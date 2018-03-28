import json
import requests
from multiprocessing import Process, Manager, Pool, cpu_count
from tqdm import tqdm
from time import time
from functools import reduce
import os

class Proxies:

    _path = os.path.join(os.path.dirname(__file__), 'proxies.json')
    _proxies = []
    _processes = cpu_count()*4
    _test_timeout = 3
    _proxy_timeout = 10

    def __init__(self, proxy_test_server, https_only=True, remote=True):

        self.https_only = https_only
        self._server = proxy_test_server

        with open(self._path) as f:
            proxies_list = json.load(f)

        if remote:
            with Pool(self._processes) as p:
                self._proxies = list(filter(lambda x: x!=False, tqdm(p.imap(self._test_connection, proxies_list), total=len(proxies_list), desc="Testing proxies", leave=True)))

        self.put({
            "local":True,
            "start":0
        })

        print("Enabled proxies: %s"%len(self._proxies))

    def _test_connection(self, proxy):
        if self.https_only and "https" in proxy["type"]:
            pass
        else:
            try:
                proxies = self._proxy_to_urls(proxy)
                requests.get(self._server, proxies = proxies, timeout=self._test_timeout)
                return proxies
            except Exception as e:
                pass
        return False

    def _proxy_to_urls(self, proxyInfo):
        url = "://%s:%s"%(proxyInfo["ip"], proxyInfo["port"])
        proxy = {
            "local":False,
            "urls":{},
            "start":0
        }

        if "http" in proxyInfo["type"]:
            proxy["urls"].update({
                "http": "http%s"%url
            })

        if "https" in proxyInfo["type"]:
            proxy["urls"].update({
                "https": "https%s"%url
            })
        return proxy

    def get(self):
        proxy = self._proxies.pop()
        if proxy["start"]==0:
            timeout = 0
        else:
            timeout = max(0, self._proxy_timeout - (time()-proxy["start"]))
        proxy["start"] = time()
        return proxy, timeout

    def put(self, proxy):
        return self._proxies.append(proxy)

    def empty(self):
        return len(self._proxies)==0