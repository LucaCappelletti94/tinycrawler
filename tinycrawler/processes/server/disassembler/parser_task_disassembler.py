"""Define a process to create parser tasks."""
from .task_disassembler import TaskDisassembler
from ....expirables import ParserTask
from ..parser_task_handler import ParserTaskHandler


class ParserTaskDisassembler(ParserTaskHandler, TaskDisassembler):
    """Define a process to create parser tasks."""

    def _job(self, *args):
        task = args[0]
        assert isinstance(task, ParserTask)
        if task.succeded:
            with open(task.path, "w") as f:
                f.write(task.page)
        return ()
