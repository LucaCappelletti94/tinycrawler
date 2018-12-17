from .sporadic_expirable import SporadicExpirable
from ..collections import Sequential
from ..exceptions import IllegalArgumentError, UnavailableError
from collections import ChainMap
import json


class SporadicSequentialExpirable(SporadicExpirable, Sequential):
    def __init__(self, **kwargs):
        """Create sporadically available, sequentially usable and expirable object.
            use_timeout:float, unavailability timeout after use.
            used_timeout:float, unavailability timeout after used.
            maximum_usages:int, maximum parallel usages.
            maximum_consecutive_errors:int, maximum number of consecutive errors before object expires.
            maximum_error_rate:float, maximum threshold of error/attempts before the object expires.
        """
        super(SporadicSequentialExpirable, self).__init__(**kwargs)

    def is_available(self, **kwargs):
        return all([
            base.is_available(self) for base in SporadicSequentialExpirable.__bases__
        ])

    def use(self, **kwargs):
        super(SporadicSequentialExpirable, self).use(**kwargs)

    def used(self, **kwargs):
        super(SporadicSequentialExpirable, self).used(**kwargs)

    def ___repr___(self):
        return {**dict(ChainMap(*[
            base.___repr___(self) for base in SporadicSequentialExpirable.__bases__
        ])), **{
            "SporadicSequentialExpirable_available": SporadicSequentialExpirable.is_available(self)
        }}
