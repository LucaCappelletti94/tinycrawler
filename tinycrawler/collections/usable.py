import abc


class Usable(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        pass

    @abc.abstractmethod
    def used(self, **kwargs):
        """Define what to do after object has been used."""

    @abc.abstractmethod
    def use(self):
        """Define what to do when object is used."""
