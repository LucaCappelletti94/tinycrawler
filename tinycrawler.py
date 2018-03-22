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
from bs4 import BeautifulSoup, SoupStrainer

import sys


class TinyCrawler:
    def __init__(self, url_seed, directory="../downloaded_websites"):
        self.urls = [url_seed]
        self.startingDomain = self.get_domain(url_seed)
        self.minTime = 5000
        self.maxTime = 10000
        self.directory = directory
        self.custom_url_filter = lambda url: True
        logging.basicConfig(filename=self.directory+"/"+self.startingDomain+'.log',level=logging.ERROR)


    def clean_request(self, text):
        soup = BeautifulSoup(text, 'lxml')
        for useless_tag in ["form", "script", "head", "style", "input"]:
            [s.extract() for s in soup(useless_tag)]
        clean_text = soup.get_text()
        clean_text = " ".join(clean_text.split())
        return clean_text

    def get_domain(self, url):
        parsed_uri = urlparse(url)
        return '{uri.netloc}'.format(uri=parsed_uri)

    def extract_urls(self, base_url, text):
        response = []
        soup = BeautifulSoup(text, "lxml", parse_only=SoupStrainer('a', href=True))
        for link in soup.find_all('a'):
            url = urljoin(base_url, link["href"])
            if self.url_filter(url):
                response.append(url)
        return response

    def parse_url(self, url):
        domain = self.get_domain(url)
        directory = self.directory+"/"+domain

        path = urlparse(url).path
        path = ''.join(e for e in path if e.isalnum())
        full_path = directory+"/"+domain+"-"+path
        filename = full_path[:100]+".json"

        if os.path.isfile(filename):
            with open(filename) as json_data:
                data = json.load(json_data)
            if url == data["url"]:
                response = []
                for saved_url in data["outgoing_urls"]:
                    if self.url_filter(saved_url):
                        response.append(saved_url)
                return response, False

        try:
            r = requests.get(url)
        except requests.exceptions.ConnectionError as e:
            return [], True

        if 'text/html' not in r.headers['content-type']:
            return [], True

        if not os.path.exists(directory):
            os.makedirs(directory)

        data = {
            "timestamp":time.time(),
            "url": url,
            "outgoing_urls": self.extract_urls(url, r.text),
            "content": self.clean_request(r.text)
        }

        with open(filename, 'w') as outfile:
            json.dump(data, outfile)

        return data["outgoing_urls"], True

    def url_filter(self, url):
        useless_words = ["#", "forum"]
        for useless_word in useless_words:
            if useless_word in url:
                return False

        return validators.url(url) and self.startingDomain == self.get_domain(url) and self.custom_url_filter(url) and url not in self.urls

    def set_url_filter(self, function):
        self.custom_url_filter = function

    def run(self):
        t = tqdm(self.urls, desc=self.startingDomain, leave=True)
        for url in t:
            ts = time.time()
            wait = True
            try:
                new_urls, wait = self.parse_url(url)
                self.urls += new_urls
            except Exception as e:
                logging.exception("Domain: "+self.startingDomain+", Current url: "+url)
                pass

            if wait:
                te = time.time()
                t.refresh()
                delta = random.randint(self.minTime,self.maxTime)/1000-te+ts
                if delta > 0:
                    time.sleep(delta)


myCrawler = TinyCrawler(sys.argv[1])

myCrawler.run()