from .expirable import Expirable
from ..collections import Sporadic
from collections import ChainMap


class SporadicExpirable(Sporadic, Expirable):
    def is_available(self, **kwargs)->bool:
        return all([
            base.is_available(self, **kwargs) for base in SporadicExpirable.__bases__
        ])

    def ___repr___(self)->dict:
        return {**dict(ChainMap(*[
            base.___repr___(self) for base in SporadicExpirable.__bases__
        ])), **{
            "SporadicExpirable_available": SporadicExpirable.is_available(self)
        }}
