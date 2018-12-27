"""Define a process to create parser tasks."""
from .task_disassembler import TaskDisassembler
from ....expirables import ParserTask, Response
from typing import Tuple
from ..parser_task_handler import ParserTaskHandler


class ParserTaskDisassembler(ParserTaskHandler, TaskDisassembler):
    """Define a process to create parser tasks."""
