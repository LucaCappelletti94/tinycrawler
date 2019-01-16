"""Create a new manager of parser task assembler processes."""
from .task_assembler_manager import TaskAssemblerManager
from ....processes.server.parser_task_handler import ParserTaskHandler
from ....processes import ParserTaskAssembler


class ParserTaskAssemblerManager(ParserTaskHandler, TaskAssemblerManager):
    """Create a new manager of parser task assembler processes."""

    def spawn(self)->ParserTaskAssembler:
        """Spawn a new ParserTaskAssembler process."""
        return ParserTaskAssembler(
            **super(ParserTaskAssemblerManager, self)._kwargs,
            responses=self._responses
        )

    def can_spawn(self)->bool:
        """Return a boolean representing if a new parser task assembler process can be spawned."""
        return self._responses.size() > 500 * self.size
