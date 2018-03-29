import os
import json
import validators
from multiprocessing import Manager, Pool
from urllib.parse import urlparse

from .trie.trie import Trie

class Urls:

    _parsed_number = 0

    _working = []
    _unparsed = []
    _custom_validator = lambda self, url: True
    _opt = {
    	"domain_fucus_only":True
    }

    def __init__(self, seed, directory, cache = True):
        self._path = "%s/urls"%directory
        self._seed = seed
        self._cache = cache
        self._url_trie = Trie(self._path+"/url_trie.pkl", cache=cache)
        self._seed_domain = Urls.domain(self._seed)

        if not os.path.exists(self._path):
            os.makedirs(self._path)

    def _is_cached(self):
        return self._cache and os.path.isfile(self._path)

    def _load_cache(self):
        with open(self._path+"/urls.json") as f:
            data = json.load(f)

        self._unparsed= list(filter(lambda u: self.valid(u), data["unparsed"]))

    def _update_cache(self):
        if self._cache:
            with open(self._path+"/urls.json", 'w') as f:
                json.dump({
                    "unparsed":self._working+self._unparsed
                }, f)

    def set_validation_options(self, opt):
    	self._opt = {**self._opt, **opt}

    def get(self):
        url = self._unparsed.pop()
        self._working.append(url)
        self._update_cache()
        return url

    def mark_done(self, url):
        self._working.remove(url)
        self._parsed_number++
        self._update_cache()

    def add(self, url):
        if self.valid(url):
            self._unparsed.append(url)
            self._url_trie.add(url)

    def _focus(self, url):
    	if self._opt["domain_fucus_only"]:
    		return self._seed_domain == Urls.domain(url)
    	return True

    def valid(self, url):
        return self._custom_validator(url) and self._focus(url) and url not in self._url_trie

    def set_custom_validator(self, validator):
        self._custom_validator = validator

    def empty(self):
        return len(self._unparsed)==0

    def add_list(self, urls):
        list(map(self.add, urls))
        self._update_cache()

    def total(self):
        return self._parsed_number + len(self._unparsed)

    def done(self):
        return self._parsed_number

    def domain(url):
        return '{uri.netloc}'.format(uri=urlparse(url))

    def load(self):
        if self._is_cached():
            self._load_cache()
        self.add(self._seed)
        self._update_cache()


