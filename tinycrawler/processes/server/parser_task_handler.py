"""Define abstract class for parser task handler."""
from ...expirables import ExpirablesQueue, Response


class ParserTaskHandler:
    """Define abstract class for parser task handler."""

    def __init__(self, **kwargs):
        """Define abstract class for parser task handler."""
        super(ParserTaskHandler, self).__init__(**kwargs)
        responses = kwargs["responses"]
        assert isinstance(responses, ExpirablesQueue)
        assert responses.type == Response
        self._responses = responses
