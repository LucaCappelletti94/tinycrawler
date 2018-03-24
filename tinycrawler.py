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

    def _get_clean_text(self, soup):
        for useless_tag in ["form", "script", "head", "style", "input"]:
            [s.extract() for s in soup(useless_tag)]
        clean_text = soup.get_text()
        clean_text = " ".join(clean_text.split())
        return clean_text

    def _get_domain(self, url):
        parsed_uri = urlparse(url)
        return '{uri.netloc}'.format(uri=parsed_uri)

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

    def _download_new_webpage(self, url, proxy, path):
        self.wait = True

        try:
            request = requests.get(url, proxies = self._proxy_to_urls(proxy))
        except Exception as e:
            return False

        if self._request_is_binary(request):
            return []

        soup = BeautifulSoup(request.text, 'lxml')

        new_urls = self._urls_from_soup(url, soup)

        self.urls.add_list(new_urls)

        self._cache_webpage(url, path, new_urls, soup)

        return new_urls

    def _load_cached_webpage(self, path):
        self.wait = False
        return self._load_cached_urls(path)

    def _parse_url(self, url_proxy_tuple):
        url = url_proxy_tuple[0]
        proxy = url_proxy_tuple[1]
        path = self._get_url_path(url)

        if self._is_path_cached(path):
            return self._load_cached_webpage(path)

        return self._download_new_webpage(url, proxy, path)

    def _sleep(self, start):
        if self.wait:
            self.sleep_time = random.randint(self.min_time,self.max_time)/1000-time.time()+start
            if self.sleep_time > 0:
                time.sleep(self.sleep_time)

    def _update_stored_urls(self):
        with open(self._urlsPath, 'w') as outfile:
            json.dump({
                "url_number":self.url_number,
                "urls":self.urls
            }, outfile)

    def _get_proxy_url_map(self):
        proxy_urls_map = []
        for i, url in enumerate(self.urls[self.url_number: min(self.url_number + len(self.proxy_list), len(self.urls))]):
            proxy_urls_map.append((url, self.proxy_list[i]))

        return proxy_urls_map

    def _iterate(self, proxy_urls_map):
        with multiprocessing.Pool(self.thread_number) as p:
            new_urls_chunks = list(p.imap(self._parse_url, proxy_urls_map))
        new_urls = [item for items in new_urls_chunks for item in items]
        for new_url in new_urls:
            if self._url_filter(new_url):
                self.to_be_parsed_urls.append(new_url)
        self._update_stored_urls()

        self.url_number+=len(proxy_urls_map)

    def set_url_filter(self, function):
        self.urls.set_url_filter(function)

    def run(self, iterations_number = -1):
        while (self.url_number < iterations_number or iterations_number == -1) and  self.url_number < len(self.urls):
            start = time.time()
            self._iterate(self._get_proxy_url_map())
            self._update_estimated_time(start)
            self._sleep(start)
            self._update_bar()

def myCustomFilter(url):
    for unwanted_word in ["#", "forum"]:
        if unwanted_word in url:
            return False
    return True

myCrawler = TinyCrawler(sys.argv[1])

myCrawler.set_url_filter(myCustomFilter)

myCrawler.run()