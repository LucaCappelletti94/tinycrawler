"""Handle UrlJob."""
from .job import Job
from ..bloom import Bloom


class UrlJob(Job):
    """Handle UrlJob."""

    def __init__(self, statistics, bloom_filters_number: int, bloom_filters_capacity: int):
        super().__init__("urls", statistics)
        self._bloom = Bloom(n=bloom_filters_number,
                            capacity=bloom_filters_capacity)

    def _update_put_statistics(self, value):
        super()._update_put_statistics(value)
        self._statistics.add(self._name, "Total %s" % self._name)

    def put(self, value):
        """Add element to jobs using dictionary keys."""
        if value not in self._bloom:
            self._bloom.put(value)
            super().put(value)
