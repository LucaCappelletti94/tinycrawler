from .usable import Usable
from ..exceptions import InUseError, NotInUseError


class Sequential(Usable):
    def __init__(self, **kwargs):
        super(Sequential, self).__init__(**kwargs)
        self._in_use = False

    def used(self, **kwargs):
        if not self._in_use:
            raise NotInUseError()
        self._in_use = False

    def use(self, **kwargs):
        if self._in_use:
            raise InUseError()
        self._in_use = True
