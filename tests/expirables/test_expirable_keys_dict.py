from tinycrawler.expirables.collections.expirables_keys_dict import ExpirableKeysDict
from tinycrawler import Domain
from .test_domain import setup as domain_setup
from ..commons import mock_repr


def setup():
    expirable_dict = ExpirableKeysDict(Domain, object)
    expirable_dict[domain_setup()] = domain_setup()
    return expirable_dict


def test_expirable_keys_dict():
    try:
        ExpirableKeysDict(str, str)
    except AssertionError:
        pass

    d = ExpirableKeysDict(Domain, object)

    try:
        d.get("test")
        assert False
    except NotImplementedError:
        pass

    try:
        "test" in d
    except AssertionError:
        pass

    domain = domain_setup()

    try:
        d.setdefault(domain, 0)
        assert False
    except NotImplementedError:
        pass

    d[domain] = "test"
    d.use(domain)

    assert d[domain] == "test"

    d.used(domain, success=False)

    try:
        d[domain] = 0
    except AssertionError:
        pass

    del d[domain]


def test_expirable_keys_dict_repr():
    mock_repr(setup())
