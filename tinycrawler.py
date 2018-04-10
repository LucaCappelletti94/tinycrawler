from multiprocessing.managers import BaseManager

from tinycrawler.log.log import log
from tinycrawler.statistics.statistics import statistics
from tinycrawler.file.file_handler import file_handler
from tinycrawler.downloader.downloader import downloader
from tinycrawler.urls.triequeue import triequeue
from tinycrawler.proxies.proxiesqueue import proxiesqueue

class MyManager(BaseManager): pass
MyManager.register('statistics', statistics)
MyManager.register('log', log)

class TinyCrawler:

    def __init__(self, seed, directory = "downloaded_websites"):

    	self._myManager = MyManager()
        self._myManager.start()

        files = Queue()
		urls = triequeue()
		stat = self._myManager.statistics()
		logger = self._myManager.log()

		self._domain = self.domain(seed)
		self._directory = "%s/%s"%(directory, self._domain)

		if not os.path.exists(self._directory):
            os.makedirs(self._directory)

        self._file_handler = file_handler(
        	files = files,
        	urls = urls,
        	path = self._directory,
        	statistics = statistics,
        )
        self._downloader = downloader(
        	urls = urls,
        	proxies = proxiesqueue(proxy_test_server = seed),
        	files = files,
        	statistics = statistics,
        	logger = logger
        )

        urls.put(seed)

    def run(self):
    	self._cli.run()
    	self._downloader.run()
    	self._file_handler.run()

    def domain(self, url):
        return '{uri.netloc}'.format(uri=urlparse(url))