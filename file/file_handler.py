from multiprocessing import Queue

class file_hanlder:

    def __init__(self, files, urls, statistics, path, timeout = 30):

        parsed = Queue()
        graph = Queue()

        self._parser = file_parser(
            files = files,
            parsed = parsed,
            urls = urls,
            graph = graph,
            statistics = statistics,
            timeout = timeout
        )
        self._webpages_writer = file_writer(parsed, "%s/%s"%(path, "webpages"), timeout)
        self._graph_writer = file_writer(graph, "%s/%s"%(path, "graph"), timeout)

    def run(self):
        """Starts the parser"""
        self._parser.run()
        self._webpages_writer.run()
        self._graph_writer.run()

    def join(self):
        self._parser.join()
        self._webpages_writer.join()
        self._graph_writer.join()