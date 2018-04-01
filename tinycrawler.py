import requests
import time
from urllib.parse import urljoin, urlparse
import os
import json
import validators

from bs4 import BeautifulSoup

import hashlib

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
MyManager.register('Log', Log)

class TinyCrawler:

    _processes_number = cpu_count()*8*2
    _headers =  {
        'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/45.0.2454.101 Safari/537.36'),
    }

    def __init__(self, seed, proxy_test_server, remote = True, cache=True, cache_timeout = 100, directory = "downloaded_websites"):
        self._domain = Urls.domain(seed)
        self._directory = "%s/%s"%(directory, self._domain)
        self._graph_path = self._directory+"/graph"
        self._webpages_path = self._directory+"/webpages"

        if not os.path.exists(self._directory):
            os.makedirs(self._directory)
        if not os.path.exists(self._webpages_path):
            os.makedirs(self._webpages_path)
        if not os.path.exists(self._graph_path):
            os.makedirs(self._graph_path)

        self._retrieve_public_ip()

        self._cache = cache

        self._myManager = MyManager()
        self._myManager.start()
        self._urls = self._myManager.Urls(
            seed = seed,
            directory=self._directory,
            cache = cache,
            cache_timeout = cache_timeout
        )
        self._logger = self._myManager.Log(directory=self._directory)
        self._proxies = self._myManager.Proxies(
            proxy_test_server = proxy_test_server,
            cache = cache,
            cache_timeout = cache_timeout,
            remote = remote
        )
        self._bar = self._myManager.Bar(
            domain = self._domain,
            total_proxies = self._proxies.total_proxies(),
            total_daemons = self._processes_number
        )

        self.proxy_lock = Lock()
        self.url_lock = Lock()

    def _get_clean_text(self, soup):
        for useless_tag in ["form", "script", "head", "style", "input"]:
            [s.extract() for s in soup(useless_tag)]
        clean_text = soup.get_text()
        clean_text = " ".join(clean_text.split())
        return clean_text

    def _retrieve_public_ip(self):
        self._ip = requests.get('http://ip.42.pl/raw').text

    def _urls_from_soup(self, base, soup):
        urls = []
        for link in soup.find_all('a', href=True):
            url = urljoin(base, link["href"])
            if validators.url(url) and "#" not in url:
                urls.append(url)
        return urls

    def _is_ip_blocked(self, text):
        if self._ip in text:
            print("IP has been flagged!!")
            self._logger.log("IP has been flagged!!")
            return True
        return False

    def _get_url_hash(self, url):
        return hashlib.md5(urlparse(url).path.encode('utf-8')).hexdigest()

    def _is_path_cached(self, url_hash):
        return self._cache and os.path.isfile("%s/%s.json"%(self._webpages_path, url_hash))

    def _load_cached_urls(self, url_hash):
        with open("%s/%s.json"%(self._webpages_path, url_hash), 'r') as json_data:
            return json.load(json_data)["outgoing"]

    # Returns true if the requested file is a binary (video, image, pdf)
    # Returns false if the file is a text file.
    def _request_is_binary(self, request):
        return 'text/html' not in request.headers['content-type']

    def _download(self, url, url_hash):
        attempts = 0
        new_urls = []
        binary = True
        while attempts<10:
            # If there are no free proxies, we sleep
            self.proxy_lock.acquire()
            if self._proxies.empty():
                self.proxy_lock.release()
                time.sleep(0.1)
            else:
                # When there is one, we aquire lock
                proxy,timeout = self._proxies.get()
                self.proxy_lock.release()
                time.sleep(timeout)

                try:
                    if proxy["local"]:
                        request = requests.get(url, headers=self._headers)
                    else:
                        request = requests.get(url, headers=self._headers, proxies = proxy["urls"])
                    success = True
                except Exception as e:
                    self._logger.exception(e)
                    time.sleep(1)
                    attempts+=1
                    success = False

                if success:
                    if self._request_is_binary(request):
                        binary = True
                    else:
                        binary = False
                        soup = BeautifulSoup(request.text, 'lxml')

                        new_urls = self._urls_from_soup(url, soup)

                        text = self._get_clean_text(soup)

                        self._is_ip_blocked(text)

                        with open("%s/%s.json"%(self._webpages_path, url_hash), 'w') as webpage_file:
                            json.dump({
                                "timestamp":time.time(),
                                "url": url,
                                "content": text
                            }, webpage_file)

                        # if self._cache:
                        #     with open("%s/%s.json"%(self._graph_path, url_hash), 'w') as urls_file:
                        #         json.dump({
                        #             "url":url,
                        #             "outgoing":new_urls
                        #             }, urls_file)

                self._proxies.put(proxy)

                if success:
                    break

        self.url_lock.acquire()
        self._urls.mark_done(url)
        if not binary:
            self._urls.add_list(new_urls)
        self.url_lock.release()

    def _job(self):
        try:
            time.sleep(1)
            i = 100
            while i > 0:
                self.url_lock.acquire()
                if not self._urls.empty():
                    url = self._urls.get()
                    self.url_lock.release()

                    i = 100

                    url_hash = self._get_url_hash(url)

                    if self._is_path_cached(url_hash):
                        pass
                        # cached_urls = self._load_cached_urls(url_hash)
                        # self.url_lock.acquire()
                        # self._urls.add_list(cached_urls)
                        # self.url_lock.release()
                    else:
                        self._download(url,url_hash)

                    self._bar.update(
                        free_proxies = self._proxies.free_proxies(),
                        parsed_urls = self._urls.done(),
                        total_urls = self._urls.total(),
                        cache_update_time = self._urls.time_to_next_caching()
                    )
                else:
                    self.url_lock.release()
                    i-=1
                    time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            self._logger.exception(e)
            raise e

    def set_validation_options(self, opt):
        self._urls.set_validation_options(opt)

    def set_custom_validator(self, function):
        self._urls.set_custom_validator(function)

    def run(self):
        self._urls.load()
        if self._urls.empty():
            self._bar.finalize()
            print("No urls to parse")
        else:
            try:
                processes = []
                self._bar.update(
                    free_proxies = self._proxies.free_proxies(),
                    parsed_urls = self._urls.done(),
                    total_urls = self._urls.total(),
                    cache_update_time = self._urls.time_to_next_caching()
                )
                for i in range(self._processes_number):
                    p = Process(target=self._job)
                    p.start()
                    processes.append(p)

                for p in processes:
                    p.join()
                self._bar.finalize()
                print("\n No more urls.")
            except KeyboardInterrupt:
                self._bar.finalize()
                print("Exiting...")
            except Exception as e:
                self._bar.finalize()
                raise e
