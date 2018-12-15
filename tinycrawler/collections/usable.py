import abc


class Usable(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        self._usages = 0

    @abc.abstractmethod
    def used(self, **kwargs):
        """Define what to do after object has been used."""
        self._usages += 1

    @abc.abstractmethod
    def use(self):
        """Define what to do when object is used."""

    def __repr__(self):
        return {
            "usages": self._usages
        }
