import abc
import json
from ..exceptions import UnavailableError
from ..utils import Printable


class Usable(Printable):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        pass

    @abc.abstractmethod
    def used(self, **kwargs):
        """Define what to do after object has been used."""

    @abc.abstractmethod
    def is_available(self, **kwargs)->bool:
        """Define if object is available."""

    @abc.abstractmethod
    def use(self, **kwargs):
        """Define what to do when object is used."""
        if not self.is_available(**kwargs):
            raise UnavailableError()

    def ___repr___(self):
        return {}
