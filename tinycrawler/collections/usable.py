"""Define an usable available object."""
import abc
from ..utils import Printable
from typing import Dict


class Usable(Printable):
    """Define an usable available object."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        """Define an usable available object."""

    @abc.abstractmethod
    def used(self, **kwargs):
        """Define what to do after object has been used."""

    @abc.abstractmethod
    def is_available(self, **kwargs)->bool:
        """Define if object is available."""

    @abc.abstractmethod
    def use(self, **kwargs):
        """Define what to do when object is used."""
        assert self.is_available(**kwargs)

    def ___repr___(self)->Dict:
        """Return a dictionary representing the object."""
        return {}
