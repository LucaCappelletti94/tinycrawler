from ...exceptions import IllegalArgumentError
from .expirables_keys_dict import ExpirableKeysDict
from ..web import Domain


class DomainsDict(ExpirableKeysDict):
    def __init__(self, *args, **kwargs):
        super(DomainsDict, self).__init__(Domain)
