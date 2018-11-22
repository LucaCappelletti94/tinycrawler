"""Handle UrlJob."""
from .job import Job
from pybloom_live import BloomFilter
from ..statistics import Statistics
from ..log import Log
import traceback


class UrlJob(Job):
    """Handle UrlJob."""

    def __init__(self, logger: Log, statistics: Statistics, bloom_filters_capacity: int):
        super().__init__("Urls queue", "urls", logger, statistics)
        self._bloom = BloomFilter(
            capacity=bloom_filters_capacity
        )

    def _update_put_statistics(self, values):
        super()._update_put_statistics(values)
        self._statistics.add(
            self._name, "Total {name}".format(name=self._name), value=len(values))

    def put(self, values: list):
        """Add element to jobs using dictionary keys."""
        self._lock.acquire()
        new_values = []
        for value in values:
            if value not in self._bloom:
                self._bloom.add(value)
                new_values.append(value)
        self._lock.release()
        try:
            super().put(new_values)
        except Exception as e:
            self._logger.error(
                "URLJOB PUT ERROR EXCEPTION GUARDA QUA: %s" % (traceback.format_exc()))
            raise e
