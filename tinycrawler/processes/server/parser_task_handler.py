"""Define abstract class for parser task handler."""
from ...expirables import ExpirablesQueue


class ParserTaskHandler:
    """Define abstract class for parser task handler."""

    def __init__(self, responses: ExpirablesQueue, **kwargs):
        """Define abstract class for parser task handler.
            responses: ExpirablesQueue, queue of responses to use for parser tasks.
        """
        super(ParserTaskHandler, self).__init__(**kwargs)
        self._responses = responses
