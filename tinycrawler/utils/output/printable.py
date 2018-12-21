import json


class Printable(object):
    def ___repr___(self):
        raise NotImplementedError(
            "Classes extending Printable should implement their ___repr___ method.")

    def __repr__(self):
        return json.dumps(self.___repr___(), indent=4, sort_keys=True)

    __str__ = __repr__
