"""Handle UrlJob."""
from .job import Job
from ..bloom import Bloom


class UrlJob(Job):
    """Handle UrlJob."""

    def __init__(self, statistics):
        super().__init__("urls", statistics)
        self._hash = self._default_hash
        self._bloom = Bloom()

    def _update_put_statistics(self, value):
        super()._update_put_statistics(value)
        self._statistics.add(self._name, "Total %s" % self._name)

    def _default_hash(self, value):
        """Return the hash of given value. Default is self."""
        return value

    def set_hash(self, _hash):
        """Set hash function."""
        self._hash = _hash

    def put(self, value):
        """Add element to jobs using dictionary keys."""
        key = self._hash(value)
        if key not in self._bloom:
            self._bloom.put(value)
            super().put(value)
