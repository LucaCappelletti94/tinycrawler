"""Handle FileJob."""
from ..statistics import Speed, Statistics
from .job import Job
from ..log import Log


class FileJob(Job):
    """Handle FileJob."""

    def __init__(self, statistics: Statistics):
        super().__init__("Pages", "pages", statistics)
        self._growing_data_speed = Speed("B")
        self._shrinking_data_speed = Speed("B")

    def _update_put_statistics(self, values):
        super()._update_put_statistics(values)
        self._statistics.add(
            self._name, "Total {name}".format(name=self._name), value=len(values))
        self._growing_data_speed.update(
            sum([len(str(value)) for value in values])
        )
        self._statistics.set(self._name, "Growing data speed",
                             self._growing_data_speed.get_formatted_speed())

    def _update_get_statistics(self, value):
        super()._update_get_statistics(value)
        self._shrinking_data_speed.update(len(str(value)))
        self._statistics.set(
            self._name, "Shrinking data speed", self._shrinking_data_speed.get_formatted_speed())
