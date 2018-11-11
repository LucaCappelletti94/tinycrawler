"""Handle FileJob."""
from ..statistics import Speed, Statistics
from .job import Job
from ..log import Log


class FileJob(Job):
    """Handle FileJob."""

    def __init__(self, name: str, logger: Log, statistics: Statistics):
        super().__init__(name, "document", logger, statistics)
        self._growing_data_speed = Speed("B")
        self._shrinking_data_speed = Speed("B")

    def _update_put_statistics(self, value):
        super()._update_put_statistics(value)
        self._statistics.add(
            self._name, "Total {name}".format(name=self._name))
        self._growing_data_speed.update(len(value.text))
        self._statistics.set(self._name, "Growing data speed",
                             self._growing_data_speed.get_formatted_speed())

    def _update_get_statistics(self, value):
        super()._update_get_statistics(value)
        self._shrinking_data_speed.update(len(value.text))
        self._statistics.set(
            self._name, "Shrinking data speed", self._shrinking_data_speed.get_formatted_speed())
