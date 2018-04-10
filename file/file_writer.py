import json


class file_writer(process_handler):

    def __init__(self, queue, path, timeout):
        super().__init__()
        self._queue = queue # Queue of files to write
        self._name = path.split("/")[-1]
        self._path = path # Path where to write files
        self._timeout = timeout
        self._file_number = 0
        self._counter = 0

        if not os.path.exists(path):
            os.makedirs(path)

    def _write(self):
        """Parse the downloaded files, cleans them and extracts urls"""
        if self._file_number%10000 == 0:
            self._counter +=1
            directory = "%s/%s"%(self._path, self._counter)
            if not os.path.exists(directory):
                os.makedirs(directory)

        self._file_number +=1

        filename, content = self._queue.get(timeout=self._timeout)
        with open("%s/%s/%s.json"%(self._path, self._counter, filename), "w") as f:
            json.dump(f, content)

    def run(self):
        """Starts the parser"""
        super().process("%s writer"%self._name, self._write)
        super().run()