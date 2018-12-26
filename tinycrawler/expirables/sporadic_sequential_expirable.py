"""Create an expirable object that is sporadically available and has a maximal number of parallel usages."""
from .sporadic_expirable import SporadicExpirable
from ..collections import Sequential
from collections import ChainMap


class SporadicSequentialExpirable(SporadicExpirable, Sequential):
    """Create an expirable object that is sporadically available and has a maximal number of parallel usages."""

    def is_available(self, **kwargs)->bool:
        """Return boolean representing if given object is available for use."""
        return all([
            base.is_available(self, **kwargs)
            for base in SporadicSequentialExpirable.__bases__
        ])

    def ___repr___(self):
        """Return a dictionary representation of object."""
        return {**dict(ChainMap(*[
            base.___repr___(self)
            for base in SporadicSequentialExpirable.__bases__
        ])), **{
            "SporadicSequentialExpirable_available": SporadicSequentialExpirable.is_available(self)
        }}
