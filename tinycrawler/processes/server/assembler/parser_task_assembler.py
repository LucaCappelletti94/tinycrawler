"""Define a process to create parser tasks."""
from .task_assembler import TaskAssembler
from ....expirables import ParserTask, Response
from typing import Tuple
from ..parser_task_handler import ParserTaskHandler


class ParserTaskAssembler(ParserTaskHandler, TaskAssembler):
    """Define a process to create parser tasks."""

    def _source(self)->Tuple[Response]:
        return (self._responses.pop(),)

    def _job(self, *args)->Tuple[ParserTask]:
        return (ParserTask(*args, **self._task_kwargs),)
