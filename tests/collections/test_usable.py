from tinycrawler.collections import Usable
from ..commons import mock_repr


def setup():
    return Usable()


def test_usable():
    setup()


def test_usable_repr():
    mock_repr(setup())
