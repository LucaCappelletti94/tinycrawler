from tinycrawler.collections import Usable
from ..utils import mock_repr


def setup():
    return Usable()


def test_usable():
    setup()


def test_usable_repr():
    mock_repr(setup())
