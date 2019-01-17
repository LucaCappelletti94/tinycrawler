"""Define a process to create parser tasks."""
import os
from .task_disassembler import TaskDisassembler
from ....expirables import ParserTask
from ..parser_task_handler import ParserTaskHandler
from ..downloader_task_handler import DownloaderTaskHandler


class ParserTaskDisassembler(ParserTaskHandler, DownloaderTaskHandler, TaskDisassembler):
    """Define a process to create parser tasks."""

    def _job(self, *args):
        task = args[0]
        assert isinstance(task, ParserTask)
        if task.succeded:
            self._urls.add(task.urls)
            os.makedirs(os.path.dirname(task.path), exist_ok=True)
            with open(task.path, "w") as f:
                f.write(task.page)
        return ()
