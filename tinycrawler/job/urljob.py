"""Handle UrlJob."""
from .job import Job
from ..bloom import Bloom
from ..statistics import Statistics
from ..log import Log


class UrlJob(Job):
    """Handle UrlJob."""

    def __init__(self, logger: Log, statistics: Statistics, bloom_filters_number: int, bloom_filters_capacity: int):
        super().__init__("Urls queue", "urls", logger, statistics)
        self._bloom = Bloom(n=bloom_filters_number,
                            capacity=bloom_filters_capacity)

    def _update_put_statistics(self, value):
        super()._update_put_statistics(value)
        self._statistics.add(
            self._name, "Total {name}".format(name=self._name))

    def put(self, value: str):
        """Add element to jobs using dictionary keys."""
        # if not self.contains(value):
        self._logger.log("Adding {url}".format(url=value))
        self._bloom.put(value)
        super().put(value)

    def contains(self, value: str):
        return value in self._bloom
