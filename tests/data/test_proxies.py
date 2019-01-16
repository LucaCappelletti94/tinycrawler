from tinycrawler.data import Proxies
from tinycrawler import Domain
from ..commons import mock_repr


def setup():
    return Proxies(path="test_data/raw_proxies.json")


def test_proxies():
    proxies = setup()
    assert proxies.size() == 1
    proxies.pop(Domain("https://www.youtube.com/watch?v=aVIXCdt7Ndg"))


def test_proxies_repr():
    mock_repr(setup())
