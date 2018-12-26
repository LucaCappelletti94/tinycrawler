"""Create a dict which raises an assertion error when given keys aren't domain."""
from ..collections import ExpirableKeysDict
from ..web import Domain
from typing import Type
from ...utils import Printable


class DomainsDict(ExpirableKeysDict, Printable):
    """Create a dict which raises an assertion error when given keys aren't domain."""

    def __init__(self, other: Type):
        """Create a dict which raises an assertion error when given keys aren't domain."""
        super(DomainsDict, self).__init__(Domain, other)

    def ___repr___(self):
        """Return a dictionary representation of object."""
        return {
            domain.domain: value.___repr___() for domain, value in self.items()
        }
