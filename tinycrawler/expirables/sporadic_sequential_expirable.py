from .sporadic_expirable import SporadicExpirable
from ..collections import Sequential
from collections import ChainMap


class SporadicSequentialExpirable(SporadicExpirable, Sequential):

    def is_available(self, **kwargs):
        return all([
            base.is_available(self)
            for base in SporadicSequentialExpirable.__bases__
        ])

    def use(self, **kwargs):
        super(SporadicSequentialExpirable, self).use(**kwargs)

    def used(self, **kwargs):
        super(SporadicSequentialExpirable, self).used(**kwargs)

    def ___repr___(self):
        return {**dict(ChainMap(*[
            base.___repr___(self)
            for base in SporadicSequentialExpirable.__bases__
        ])), **{
            "SporadicSequentialExpirable_available": SporadicSequentialExpirable.is_available(self)
        }}
