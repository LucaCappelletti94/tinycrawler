from ..collections import ExpirableKeysDict
from ..web import Domain
from typing import Type
from ...utils import Printable


class DomainsDict(ExpirableKeysDict, Printable):
    def __init__(self, other: Type):
        super(DomainsDict, self).__init__(Domain, other)

    def ___repr___(self):
        return {
            domain.domain: value.___repr___() for domain, value in self.items()
        }
