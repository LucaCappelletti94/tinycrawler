from tinycrawler import Domain
from .utils import mock_repr


def setup():
    return Domain("https://www.youtube.com/watch?v=LxtppUZthug")


def test_domain():
    assert setup() == setup()


def test_domain_repr():
    mock_repr(setup())
