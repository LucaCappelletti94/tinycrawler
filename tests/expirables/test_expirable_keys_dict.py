from tinycrawler.expirables.collections.expirables_keys_dict import ExpirableKeysDict
from tinycrawler import Domain
from .test_domain import setup as domain_setup
from ..commons import mock_repr
import pytest


def setup():
    expirable_dict = ExpirableKeysDict(Domain, object)
    expirable_dict[domain_setup()] = domain_setup()
    return expirable_dict


def test_expirable_keys_dict():
    with pytest.raises(AssertionError):
        ExpirableKeysDict(str, str)

    d = ExpirableKeysDict(Domain, object)

    with pytest.raises(NotImplementedError):
        d.get("test")

    with pytest.raises(AssertionError):
        "test" in d

    domain = domain_setup()

    with pytest.raises(NotImplementedError):
        d.setdefault(domain, 0)

    d[domain] = "test"
    d.use(domain)

    assert d[domain] == "test"

    d.used(domain, success=False)

    with pytest.raises(AssertionError):
        d[domain] = 0

    del d[domain]


def test_expirable_keys_dict_repr():
    mock_repr(setup())
