"""Create a new manager of parser task assembler processes."""
from .task_disassembler_manager import TaskDisassemblerManager
from ....processes.server.parser_task_handler import ParserTaskHandler
from ....processes.server.downloader_task_handler import DownloaderTaskHandler
from ....processes import ParserTaskDisassembler


class ParserTaskDisassemblerManager(ParserTaskHandler, DownloaderTaskHandler, TaskDisassemblerManager):
    """Create a new manager of parser task assembler processes."""

    def spawn(self)->ParserTaskDisassembler:
        """Spawn a new ParserTaskDisassembler process."""
        return ParserTaskDisassembler(
            **super(ParserTaskDisassemblerManager, self)._kwargs,
            responses=self._responses,
            urls=self._urls,
            proxies=self._proxies
        )
