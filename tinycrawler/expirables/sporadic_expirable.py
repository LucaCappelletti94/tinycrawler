from .expirable import Expirable
from ..collections import Sporadic
from collections import ChainMap


class SporadicExpirable(Sporadic, Expirable):
    def is_available(self, **kwargs):
        return all([
            base.is_available(self) for base in SporadicExpirable.__bases__
        ])

    def use(self, **kwargs):
        super(SporadicExpirable, self).use(**kwargs)

    def used(self, **kwargs):
        super(SporadicExpirable, self).used(**kwargs)

    def ___repr___(self):
        return {**dict(ChainMap(*[
            base.___repr___(self) for base in SporadicExpirable.__bases__
        ])), **{
            "SporadicExpirable_available": SporadicExpirable.is_available(self)
        }}
