from tinycrawler.expirables import DomainsDict
from tinycrawler import Domain, IllegalArgumentError


def test_domains_dict():
    d = DomainsDict()

    try:
        d.get("test")
        assert False
    except IllegalArgumentError:
        pass

    domain = Domain("https://travis-ci.org/LucaCappelletti94/tinycrawler")

    d[domain] = "test"
    assert d[domain] == "test"
    assert d.get(domain) == "test"
