"""Create a new manager of downloader task assembler processes."""
from .task_disassembler_manager import TaskDisassemblerManager
from ....processes.server.downloader_task_handler import DownloaderTaskHandler
from ....processes.server.parser_task_handler import ParserTaskHandler
from ....processes import DownloaderTaskDisassembler


class DownloaderTaskDisassemblerManager(ParserTaskHandler, DownloaderTaskHandler, TaskDisassemblerManager):
    """Create a new manager of downloader task assembler processes."""

    def spawn(self)->DownloaderTaskDisassembler:
        """Spawn a new DownloaderTaskDisassembler process."""
        return DownloaderTaskDisassembler(
            **super(DownloaderTaskDisassemblerManager, self)._kwargs,
            responses=self._responses,
            urls=self._urls,
            proxies=self._proxies
        )
