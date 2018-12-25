from tinycrawler.expirables import DomainsDict
from tinycrawler import Domain
from .utils import mock_repr
from .test_domain import setup as domain_setup


def setup():
    domains = DomainsDict(Domain)
    domain = domain_setup()
    domains[domain] = domain
    return domains


def test_domains_dict():
    setup()


def test_domains_dict_repr():
    mock_repr(setup())
