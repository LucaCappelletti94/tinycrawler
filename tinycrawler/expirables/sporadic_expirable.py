"""Create an expirable object that is sporadically available."""
from .expirable import Expirable
from ..collections import Sporadic
from collections import ChainMap


class SporadicExpirable(Sporadic, Expirable):
    """Create an expirable object that is sporadically available."""

    def is_available(self, **kwargs)->bool:
        """Return boolean representing if given object is available for use."""
        return all([
            base.is_available(self, **kwargs) for base in SporadicExpirable.__bases__
        ])

    def ___repr___(self)->dict:
        """Return a dictionary representation of object."""
        return {**dict(ChainMap(*[
            base.___repr___(self) for base in SporadicExpirable.__bases__
        ])), **{
            "SporadicExpirable_available": SporadicExpirable.is_available(self)
        }}
