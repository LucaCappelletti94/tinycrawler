from ...exceptions import IllegalArgumentError
from .expirables_keys_dict import ExpirableKeysDict
from ..web import Domain
from typing import Type
import json


class DomainsDict(ExpirableKeysDict):
    def __init__(self, other: Type):
        super(DomainsDict, self).__init__(Domain, other)

    def ___repr___(self):
        return {
            domain.domain: value.___repr___() for domain, value in self.items()
        }

    def __repr__(self):
        return json.dumps(self.___repr___(), indent=4, sort_keys=True)

    __str__ = __repr__
