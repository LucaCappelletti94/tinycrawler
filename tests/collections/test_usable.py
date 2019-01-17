from tinycrawler.collections import Usable
from ..commons import mock_repr


def usable_setup():
    return Usable()


def test_usable():
    usable_setup()


def test_usable_repr():
    mock_repr(usable_setup())
