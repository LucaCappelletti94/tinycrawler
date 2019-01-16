"""Create a new manager of downloader task assembler processes."""
from .task_assembler_manager import TaskAssemblerManager
from ....processes.server.downloader_task_handler import DownloaderTaskHandler
from ....processes import DownloaderTaskAssembler


class DownloaderTaskAssemblerManager(DownloaderTaskHandler, TaskAssemblerManager):
    """Create a new manager of downloader task assembler processes."""

    def spawn(self)->DownloaderTaskAssembler:
        """Spawn a new DownloaderTaskAssembler process."""
        return DownloaderTaskAssembler(
            **super(DownloaderTaskAssemblerManager, self)._kwargs,
            urls=self._urls,
            proxies=self._proxies
        )

    def can_spawn(self)->bool:
        """Return a boolean representing if a new downloader task assembler process can be spawned."""
        n = 500 * self.size
        return self._urls.size() > n and self._proxies.size() > n
