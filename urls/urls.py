import os
import json
import validators

class Urls:

    _manager = Manager()

    _parsed = _manager.list()
    _unparsed = _manager.list()
    _custom_validator = lambda url: True
    _processes = 4

    def __init__(self, seed, directory, cache=False):
        self.cache=cache
        self._path = "%s-urls.json"%_directory
        if self._is_cached():
            self._load_cache()
        else:
            self.add(seed)

    def _is_cached(self):
        return self.cache and os.path.isfile(self._path)

    def _load_cache(self):
        with open(self._path) as f:
            data = json.load(f)

        self._parsed= data["parsed"]
        self._unparsed= data["unparsed"]
        list(map(self._unparsed.put, data["unparsed"]))

    def _update_cache(self):
        with open(self._path, 'w') as f:
            json.dump({
                "parsed":self._parsed,
                "unparsed":self._unparsed
            }, f)

    def get(self):
        url = self._unparsed[0]
        self._unparsed = self._unparsed[1:]
        self.parsed.append(url)
        if self.cache:
            self._update_cache()
        return url

    def add(self, url):
        if self.valid(url):
            self._unparsed.append(url)
            if self.cache:
                self._update_cache()

    def valid(self, url):
        return self._custom_validator(url) and url not in self._parsed and url not in self._unparsed

    def set_custom_validator(self, validator):
        self._custom_validator = validator

    def empty(self):
        return not self._unparsed

    def add_list(self, urls):
        with Pool(self._processes) as p:
            p.map(self.add, urls)