"""Define a process to destroy downloader tasks."""
from .task_disassembler import TaskDisassembler
from ..downloader_task_handler import DownloaderTaskHandler


class DownloaderTaskDisassembler(DownloaderTaskHandler, TaskDisassembler):
    """Define a process to destroy downloader tasks."""

    def _sink(self, *args):
        self._urls.put(*args)
