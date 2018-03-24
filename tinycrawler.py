from tqdm import tqdm
import requests
import time
from urllib.parse import urljoin, urlparse
import random
import os
import json
import validators

from bs4 import BeautifulSoup
from multiprocessing import Process, Manager
from datetime import datetime, timedelta
import sys

from tinycrawler.log import log
from tinycrawler.proxies import proxies
from tinycrawler.bar import bar

class TinyCrawler:

    _processes_number = 8

    def __init__(self, seed, directory = "../downloaded_websites"):
        self._domain = self._get_domain(seed)
        self._directory = "%s/%s"%(self._directory, self._domain)
        if not os.path.exists(self._directory):
            os.makedirs(self._directory)

        self._logger = Log(directory=self.directory)
        self._urls = Urls(
            seed = seed,
            directory=self.directory
        )
        self._proxies = Proxies()
        self._bar = Bar()

    def _get_domain(self, url):
        parsed_uri = urlparse(url)
        return '{uri.netloc}'.format(uri=parsed_uri)

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

    def _download(self, url, path):
        # If there are no free proxies, we sleep
        while self._proxies.empty():
            time.sleep(0.1)
        # When there is one, we aquire lock
        proxy = self._proxies.get()

        try:
            request = requests.get(url, proxies = self._proxy_to_urls(proxy))
            if self._request_is_binary(request):
                return []

            soup = BeautifulSoup(request.text, 'lxml')

            new_urls = self._urls_from_soup(url, soup)

            self.urls.add_list(new_urls)

            self._cache_webpage(url, path, new_urls, soup)
        except Exception as e:
            self._logger.exception(url)
            pass

        # When we are done, we free the proxy
        self._proxies.add(proxy)


    def _load_cached_webpage(self, path):
        self.wait = False
        return self._load_cached_urls(path)


    def _job(self, lock):
        while not self._urls.empty():
            url = self._urls.get()

            path = self._get_url_path(url)

            if self._is_path_cached(path):
                self._load_cached_webpage(path)
            else:
                self._download(url,path)

            self._bar.update(self._urls.total(), self._urls.done())

    def set_url_filter(self, function):
        self.urls.set_url_filter(function)

    def run(self):
        processes = []
        lock = Lock()
        for i in range(self._processes_number):
            p = Process(target=self._job, args=(lock))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

def myCustomFilter(url):
    for unwanted_word in ["#", "forum"]:
        if unwanted_word in url:
            return False
    return True

myCrawler = TinyCrawler(sys.argv[1])

myCrawler.set_url_filter(myCustomFilter)

myCrawler.run()