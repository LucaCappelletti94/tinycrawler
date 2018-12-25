from tinycrawler.expirables import DomainsDict
from tinycrawler import Domain
from .utils import mock_repr


def setup():
    domains = DomainsDict(Domain)
    domain = Domain("http://www.totally.fake.example.com/error")
    domains[domain] = domain
    return domains


def test_domains_dict():
    setup()


def test_domains_dict_repr():
    mock_repr(setup())
