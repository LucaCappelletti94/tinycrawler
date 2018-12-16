import abc
import json


class Usable(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        pass

    @abc.abstractmethod
    def used(self, **kwargs):
        """Define what to do after object has been used."""

    @abc.abstractmethod
    def use(self, **kwargs):
        """Define what to do when object is used."""

    def ___repr___(self):
        return {}

    def __repr__(self):
        return json.dumps(self.___repr___(), indent=4, sort_keys=True)

    __str__ = __repr__
