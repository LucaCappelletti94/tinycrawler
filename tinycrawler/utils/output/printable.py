"""Define an printable object."""
import json
from typing import Dict


class Printable:
    """Define an printable object."""

    def ___repr___(self)->Dict:
        """Return a dictionary representing the object."""
        raise NotImplementedError(
            "Classes extending Printable should implement their ___repr___ method."
        )

    def __repr__(self):
        """Return a json representation of the object."""
        return json.dumps(self.___repr___(), indent=4, sort_keys=True)

    __str__ = __repr__
