from .expirable import Expirable
from ..collections import Sporadic, Sequential
from ..exceptions import InUseError, IllegalArgumentError, UnavailableError
from collections import ChainMap
import json


class SporadicSequentialExpirable(Sporadic, Sequential, Expirable):
    def __init__(self, **kwargs):
        """Create sporadically available, sequentially usable and expirable object.
            use_timeout:float, unavailability timeout after use.
            used_timeout:float, unavailability timeout after used.
            maximum_usages:int, maximum parallel usages.
            maximum_consecutive_errors:int, maximum number of consecutive errors before object expires.
            maximum_error_rate:float, maximum threshold of error/attempts before the object expires.
        """
        super(SporadicSequentialExpirable, self).__init__(**kwargs)
        if Sequential._constraints_are_active(self) and not Expirable._constraints_are_active(self) and not Sporadic._constraints_are_active(self):
            raise IllegalArgumentError(
                "Given constraint cause object to never become expired, even when Sequential constraint is active.")

    def is_available(self):
        sporadic_available = Sporadic.is_available(self)
        expirable_available = Expirable.is_available(self)
        sequential_available = Sequential.is_available(self)
        return sporadic_available and expirable_available and (sporadic_available or sequential_available)

    def use(self, **kwargs):
        if not self.is_available():
            raise UnavailableError()
        try:
            super(SporadicSequentialExpirable, self).use(**kwargs)
        except InUseError:
            self.used(success=False)

    def used(self, **kwargs):
        super(SporadicSequentialExpirable, self).used(**kwargs)

    def ___repr___(self):
        return {**dict(ChainMap(*[
            base.___repr___(self) for base in SporadicSequentialExpirable.__bases__
        ])), **{
            "SporadicSequentialExpirable_available": self.is_available()
        }}
