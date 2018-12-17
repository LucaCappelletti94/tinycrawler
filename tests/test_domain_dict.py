from tinycrawler.expirables import DomainsDict
from tinycrawler import Domain, IllegalArgumentError


def test_domains_dict():
    d = DomainsDict()

    try:
        d.get("test")
        assert False
    except NotImplementedError:
        pass

    domain = Domain("https://travis-ci.org/LucaCappelletti94/tinycrawler")

    try:
        d.setdefault(domain, 0)
        assert False
    except NotImplementedError:
        pass

    d[domain] = "test"

    assert d[domain] == "test"

    del d[domain]
