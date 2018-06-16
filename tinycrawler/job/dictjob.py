"""Handle Job dispatching with search handled with dictionary."""
from .job import Job


class DictJob(Job):
    """Handle DictJob dispatching with search handled with dictionary."""

    def __init__(self, name, statistics, logger):
        """Handle DictJob dispatching with search handled with dictionary."""
        super().__init__(name, statistics)
        self._logger = logger
        self._data = {}

    def _hash(self, value):
        """Return the hash of given value. Default is self."""
        return value

    def set_hash(self, _hash):
        """Set hash function."""
        self._hash = _hash

    def put(self, value):
        """Add element to jobs using dictionary keys."""
        key = self._hash(value)
        self._data[key] = None
        super().put(value)

    def contains(self, value):
        """Check if value is already in queue."""
        return value in self._data
