from multiprocessing import Process, Manager, Pool

class Proxies:

    _path = "proxies.json"
    _server = "http://188.152.124.186"
    _manager = Manager()
    _proxies = _manager.Queue()
    _processes = 8
    _timeout = 5

    def __init__(self):
      with open(self._path) as f:
          proxies_list = json.load(f)

      with Pool(self._processes) as p:
          p.map(self._test_connection, proxies_list)

    def _test_connection(self, proxy):
        try:
            proxies = self._proxy_to_urls(proxy)
            requests.get(self._server, proxies = proxies, timeout=self._timeout)
            self._proxies.put(proxies)
        except Exception as e:
            pass

    def _proxy_to_urls(self, proxy):
        proxyUrl = "://%s:%s"%(proxy["ip"], proxy["port"])
        if proxy["https"]:
            return {
                "http": "http%s"%proxyUrl,
                "https": "https%s"%proxyUrl
            }
        return {"http": "http%s"%proxyUrl}