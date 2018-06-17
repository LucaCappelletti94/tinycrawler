"""Handle UrlJob."""
from .dictjob import DictJob


class UrlJob(DictJob):
    """Handle UrlJob."""

    def __init__(self, statistics):
        super().__init__("url", statistics)

    def _update_put_statistics(self, value):
        super()._update_put_statistics(value)
        self._statistics.add(self._name, "Total %s" % self._name)
