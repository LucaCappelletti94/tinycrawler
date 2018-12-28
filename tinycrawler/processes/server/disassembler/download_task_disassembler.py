"""Define a process to destroy downloader tasks."""
from .task_disassembler import TaskDisassembler
from ..downloader_task_handler import DownloaderTaskHandler
from ..parser_task_handler import ParserTaskHandler
from ....expirables import DownloaderTask, Response


class DownloaderTaskDisassembler(DownloaderTaskHandler, ParserTaskHandler, TaskDisassembler):
    """Define a process to destroy downloader tasks."""

    def _job(self, *args):
        task = args[0]
        assert isinstance(task, DownloaderTask)
        if task.failed:
            url, proxy = task.data
            self._urls.add(url)
            self._proxies.add(proxy)
        elif task.binary:
            # In future this will be logged in the statistics
            pass
        elif task.succeded:
            self._responses.add(
                Response(
                    task.text,
                    task.response_status,
                    task.url
                )
            )
        return ()
