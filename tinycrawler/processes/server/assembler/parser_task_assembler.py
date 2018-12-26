from .task_assembler import TaskAssembler
from ....expirables import ExpirablesQueue, ParserTask, Response
from ....exceptions import Sleep
from queue import Empty
from typing import Tuple


class ParserTaskAssembler(TaskAssembler):
    def __init__(self, responses: ExpirablesQueue, **kwargs):
        super(ParserTaskAssembler, self).__init__(**kwargs)
        self._responses = responses

    def _source(self)->Tuple[Response]:
        try:
            return self._responses.pop()
        except Empty:
            raise Sleep

    def _job(self, response: Response)->Tuple[ParserTask]:
        return ParserTask(
            response,
            **self._task_kwargs
        )
