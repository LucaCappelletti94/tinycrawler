from ..web import Domain
from ...exceptions import IllegalArgumentError


class DomainsDict(dict):
    def __getitem__(self, k):
        return super(DomainsDict, self).__getitem__(self._ensure_domain(k))

    def __setitem__(self, k, v):
        return super(DomainsDict, self).__setitem__(self._ensure_domain(k), v)

    def __delitem__(self, k):
        return super(DomainsDict, self).__delitem__(self._ensure_domain(k))

    def get(self, k, default=None):
        return super(DomainsDict, self).get(self._ensure_domain(k), default)

    def setdefault(self, k, default=None):
        return super(DomainsDict, self).setdefault(self._ensure_domain(k), default)

    def __contains__(self, k):
        return super(DomainsDict, self).__contains__(self._ensure_domain(k))

    def __repr__(self):
        return '{0}({1})'.format(type(self).__name__, super(DomainsDict, self).__repr__())

    def _ensure_domain(self, key):
        if not isinstance(key, Domain):
            raise IllegalArgumentError("Given key is not a domain object.")
        return key
