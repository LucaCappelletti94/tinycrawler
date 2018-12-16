from .expirable import Expirable
from ..collections import Sporadic
from ..exceptions import IllegalArgumentError, UnavailableError
from collections import ChainMap
import json


class SporadicExpirable(Sporadic, Expirable):
    def __init__(self, **kwargs):
        """Create sporadically available, sequentially usable and expirable object.
            use_timeout:float, unavailability timeout after use.
            used_timeout:float, unavailability timeout after used.
            maximum_consecutive_errors:int, maximum number of consecutive errors before object expires.
            maximum_error_rate:float, maximum threshold of error/attempts before the object expires.
        """
        super(SporadicExpirable, self).__init__(**kwargs)

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
