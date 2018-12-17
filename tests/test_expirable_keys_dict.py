from tinycrawler.expirables.collections.expirables_keys_dict import ExpirableKeysDict
from tinycrawler import Domain, IllegalArgumentError, UnavailableError


def test_expirable_keys_dict():

    try:
        ExpirableKeysDict(str)
        assert False
    except IllegalArgumentError:
        pass

    d = ExpirableKeysDict(Domain)

    try:
        d.get("test")
        assert False
    except NotImplementedError:
        pass

    try:
        "test" in d
        assert False
    except IllegalArgumentError:
        pass

    domain = Domain("https://travis-ci.org/LucaCappelletti94/tinycrawler",
                    maximum_consecutive_errors=1, maximum_error_rate=0.5)

    try:
        d.setdefault(domain, 0)
        assert False
    except NotImplementedError:
        pass

    d[domain] = "test"

    assert d[domain] == "test"

    d.used(domain, success=False)

    try:
        d[domain] = 0
        assert False
    except UnavailableError:
        pass

    del d[domain]
