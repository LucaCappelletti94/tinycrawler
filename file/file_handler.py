from multiprocessing import Queue

from .file_parser import file_parser
from .file_writer import file_writer

class file_handler:

    def __init__(self, files, urls, path, statistics, logger, timeout = 30):

        parsed = Queue()
        graph = Queue()

        self._parser = file_parser(
            files = files,
            parsed = parsed,
            urls = urls,
            graph = graph,
            statistics = statistics,
            logger = logger,
            timeout = timeout
        )
        self._webpages_writer = file_writer(parsed, "%s/%s"%(path, "webpages"), statistics, logger, timeout)
        self._graph_writer = file_writer(graph, "%s/%s"%(path, "graph"), statistics, logger, timeout)

    def run(self):
        """Starts the parser"""
        self._parser.run()
        self._webpages_writer.run()
        self._graph_writer.run()

    def join(self):
        self._parser.join()
        self._webpages_writer.join()
        self._graph_writer.join()

    def set_url_validator(self, url_validator):
        self._parser.set_url_validator(url_validator)