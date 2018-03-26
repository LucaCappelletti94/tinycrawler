import requests
import time
from urllib.parse import urljoin, urlparse
import os
import json
import validators

from bs4 import BeautifulSoup

from multiprocessing import Process, Lock, cpu_count, Manager
from multiprocessing.managers import BaseManager

from tinycrawler.log.log import Log
from tinycrawler.urls.urls import Urls
from tinycrawler.proxies.proxies import Proxies
from tinycrawler.bar.bar import Bar

class MyManager(BaseManager): pass
MyManager.register('Urls', Urls)
MyManager.register('Proxies', Proxies)
MyManager.register('Bar', Bar)

class TinyCrawler:

    _processes_number = cpu_count()

    def __init__(self, seed, proxy_test_server, directory = "downloaded_websites"):
        self._domain = Urls.domain(seed)
        self._directory = "%s/%s"%(directory, self._domain)
        if not os.path.exists(self._directory):
            os.makedirs(self._directory)

        self._logger = Log(directory=self._directory)
        self._myManager = MyManager()
        self._myManager.start()
        self._urls = self._myManager.Urls(
            seed = seed,
            directory=self._directory
        )
        self._proxies = self._myManager.Proxies(
            proxy_test_server = proxy_test_server
        )
        self._bar = self._myManager.Bar(self._domain)

    def _get_clean_text(self, soup):
        for useless_tag in ["form", "script", "head", "style", "input"]:
            [s.extract() for s in soup(useless_tag)]
        clean_text = soup.get_text()
        clean_text = " ".join(clean_text.split())
        return clean_text

    def _urls_from_soup(self, base, soup):
        urls = []
        for link in soup.find_all('a', href=True):
            url = urljoin(base, link["href"])
            if validators.url(url):
                urls.append(url)
        return urls

    def _get_url_path(self, url):
        path = ''.join(e for e in urlparse(url).path if e.isalnum())
        return self._directory+"/"+path[:100]+".json"

    def _is_path_cached(self, path):
        return os.path.isfile(path)

    def _load_cached_urls(self, path):
        with open(path) as json_data:
            return json.load(json_data)["outgoing_urls"]

    def _cache_webpage(self, url, path, outgoing_urls, soup):
        with open(path, 'w') as outfile:
            json.dump({
                "timestamp":time.time(),
                "url": url,
                "outgoing_urls": outgoing_urls,
                "content": self._get_clean_text(soup)
            }, outfile)

    # Returns true if the requested file is a binary (video, image, pdf)
    # Returns false if the file is a text file.
    def _request_is_binary(self, request):
        return 'text/html' not in request.headers['content-type']

    def _download(self, url, path, lock, identifier):
        while True:
            # If there are no free proxies, we sleep
            lock.acquire()
            if self._proxies.empty():
                lock.release()
                time.sleep(0.1)
            else:
                # When there is one, we aquire lock
                proxy,timeout = self._proxies.get()
                lock.release()
                time.sleep(timeout)

                try:
                    if proxy["local"]:
                        request = requests.get(url)
                    else:
                        request = requests.get(url, proxies = proxy["urls"])
                    success = True
                except Exception as e:
                    self._logger.exception(url)
                    success = False

                if success:
                    if self._request_is_binary(request):
                        pass
                    else:
                        soup = BeautifulSoup(request.text, 'lxml')

                        new_urls = self._urls_from_soup(url, soup)

                        lock.acquire()
                        self._urls.add_list(new_urls)
                        self._cache_webpage(url, path, new_urls, soup)
                        lock.release()

                # When we are done, we free the proxy
                lock.acquire()
                self._proxies.put(proxy)
                lock.release()
                break

    def _load_cached_webpage(self, path):
        return self._load_cached_urls(path)

    def _job(self, lock, identifier):
        i = 100
        while i > 0:
            lock.acquire()
            if not self._urls.empty():
                url = self._urls.get()
                lock.release()

                i = 100

                path = self._get_url_path(url)

                if self._is_path_cached(path):
                    lock.acquire()
                    self._urls.add_list(self._load_cached_webpage(path))
                    lock.release()
                else:
                    self._download(url,path, lock, identifier)

                self._bar.update(self._urls.total(), self._urls.done())
            else:
                lock.release()
                i-=1
                time.sleep(0.1)

    def set_validation_options(self, opt):
        self._urls.set_validation_options(opt)

    def set_custom_validator(self, function):
        self._urls.set_custom_validator(function)

    def run(self):
        self._urls.load()
        if self._urls.empty():
            print("No urls to parse")
        else:
            processes = []
            lock = Lock()
            print("Processes used: %s"%self._processes_number)
            for i in range(self._processes_number):
                p = Process(target=self._job, args=(lock,i))
                p.start()
                processes.append(p)

            for p in processes:
              p.join()
