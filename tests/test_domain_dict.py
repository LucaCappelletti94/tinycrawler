from tinycrawler.expirables import DomainsDict
from tinycrawler import Domain, IllegalArgumentError


def test_domains_dict():
    d = DomainsDict(Domain)
    domain = Domain("http://www.totally.fake.example.com/error")
    d[domain] = domain

    with open("test_data/expected_domains_dict_representation.json", "r") as f:
        assert str(d) == f.read()
