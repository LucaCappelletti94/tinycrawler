import abc


class Usable(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def used(self):
        """Define what to do after object has been used."""

    @abc.abstractmethod
    def use(self):
        """Define what to do when object is used."""
