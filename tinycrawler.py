from tqdm import tqdm
import requests
import time
from urllib.parse import urljoin, urlparse
import random
import os
import json
import datetime
import validators
import logging
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

import sys


class TinyCrawler:

    minTime = 5000
    maxTime = 10000
    directory = "../downloaded_websites"
    custom_url_filter = lambda url: True
    wait = True
    url_number = 0
    estimated_step_time = 0
    max_output_len = 0
    sleep_time = 0
    estimated_sleep_time = (minTime+maxTime)/2000

    def __init__(self, url_seed):
        self.domain = self._get_domain(url_seed)
        self._init_paths()
        self._init_log()
        self._init_urls(url_seed)

    def _init_paths(self):
        self.directory = "%s/%s"%(self.directory, self.domain)
        self.urlsPath = "%s-urls.json"%(self.directory)
        self.logPath = "%s.log"%(self.directory)

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def _init_log(self):
        # If the log already exists, we clear it.
        if os.path.isfile(self.logPath):
            with open(self.logPath, 'w'):
                pass
        logging.basicConfig(filename=self.logPath,level=logging.ERROR)

    def _init_urls(self, url_seed):
        if os.path.isfile(self.urlsPath):
            with open(self.urlsPath) as json_data:
                data = json.load(json_data)
            self.urls = data["urls"]
            self.url_number = data["url_number"]
        else:
            self.urls = [url_seed]

    def _get_clean_text(self, soup):
        for useless_tag in ["form", "script", "head", "style", "input"]:
            [s.extract() for s in soup(useless_tag)]
        clean_text = soup.get_text()
        clean_text = " ".join(clean_text.split())
        return clean_text

    def _get_domain(self, url):
        parsed_uri = urlparse(url)
        return '{uri.netloc}'.format(uri=parsed_uri)

    def _extract_urls(self, base_url, soup):
        response = []
        for link in soup.find_all('a', href=True):
            url = urljoin(base_url, link["href"])
            if validators.url(url):
                response.append(url)
        return response

    def _get_url_path(self, url):
        path = ''.join(e for e in urlparse(url).path if e.isalnum())
        return self.directory+"/"+path[:100]+".json"

    def _is_path_cached(self, path):
        return os.path.isfile(path)

    def _load_cached_urls(self, path):
        with open(path) as json_data:
            return json.load(json_data)["outgoing_urls"]

    def _cache_url(self, url, path, outgoing_urls, soup):
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

    def _download_new_webpage(self, url, path):
        self.wait = True

        request = requests.get(url)

        if self._request_is_binary(request):
            return []

        soup = BeautifulSoup(request.text, 'lxml')

        new_urls = self._extract_urls(url, soup)

        self._cache_url(url, path, new_urls, soup)

        return new_urls

    def _load_cached_webpage(self, path):
        self.wait = False
        return self._load_cached_urls(path)

    def _parse_url(self, url):
        path = self._get_url_path(url)

        if self._is_path_cached(path):
            return self._load_cached_webpage(path)

        return self._download_new_webpage(url, path)

    def _url_filter(self, url):
        return self.domain == self._get_domain(url) and self.custom_url_filter(url) and url not in self.urls

    def _sleep(self, start):
        if self.wait:
            self.sleep_time = random.randint(self.minTime,self.maxTime)/1000-time.time()+start
            if self.sleep_time > 0:
                time.sleep(self.sleep_time)

    def _update_stored_urls(self):
        with open(self.urlsPath, 'w') as outfile:
            json.dump({
                "url_number":self.url_number,
                "urls":self.urls
            }, outfile)

    def _iterate(self, url):
        try:
            for new_url in self._parse_url(url):
                if self._url_filter(new_url):
                    self.urls.append(new_url)
            self._update_stored_urls()
        except Exception as e:
            logging.exception("Domain: "+self.domain+", Current url: "+url)
            pass

    def _estimated_time(self):
        d = datetime(1,1,1) + timedelta(seconds=(self.estimated_step_time+self.estimated_sleep_time)*(len(self.urls)-self.url_number))
        response = ""
        if d.day-1>0:
            response += "%sd"%(d.day-1)

        if d.hour>0:
            if response != "":
                response+=", "
            response += "%sh"%(d.hour)

        if d.minute>0:
            if response != "":
                response+=", "
            response += "%sm"%(d.minute)

        if d.second>0:
            if response != "":
                response+=", "
            response += "%ss"%(d.second)
        return response

    def _update_estimated_time(self, start):
        self.estimated_step_time = self.estimated_step_time*0.5 + 0.5*(time.time()-start)
        self.estimated_sleep_time = self.estimated_sleep_time*0.5 + 0.5*self.sleep_time

    def _update_bar(self):
        output = "%s: %s/%s. ETA: %s, 1it in %ss, sleeping for %ss"%(self.domain, self.url_number, len(self.urls), self._estimated_time(), round(self.estimated_step_time, 1), round(self.estimated_sleep_time, 1))
        if len(output)>self.max_output_len:
            self.max_output_len = len(output)
        output += " "*(self.max_output_len-len(output))
        print (output, end="\r")
        sys.stdout.flush()

    def set_url_filter(self, function):
        self.custom_url_filter = function

    def run(self, iterations_number = -1):
        while (self.url_number < iterations_number or iterations_number == -1) and  self.url_number < len(self.urls):
            start = time.time()
            self._iterate(self.urls[self.url_number])
            self._update_estimated_time(start)
            self._sleep(start)
            self._update_bar()
            self.url_number+=1

def myCustomFilter(url):
    for unwanted_word in ["#", "forum"]:
        if unwanted_word in url:
            return False
    return True

myCrawler = TinyCrawler(sys.argv[1])

myCrawler.set_url_filter(myCustomFilter)

myCrawler.run()