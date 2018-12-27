"""Define abstract class for parser task handler."""


class ParserTaskHandler:
    """Define abstract class for parser task handler."""

    def __init__(self, **kwargs):
        """Define abstract class for parser task handler."""
        super(ParserTaskHandler, self).__init__(**kwargs)
        self._responses = kwargs["responses"]
