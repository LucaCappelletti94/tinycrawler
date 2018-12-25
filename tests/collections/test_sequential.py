from tinycrawler.collections import Sequential
from ..utils import mock_repr


def setup():
    return Sequential(maximum_usages=1)


def test_sequential():
    sequential = setup()
    try:
        sequential.used()
        assert False
    except AssertionError:
        pass
    sequential.use()
    try:
        sequential.use()
        assert False
    except AssertionError:
        pass

    sequential.used()


def test_sequential_repr():
    mock_repr(setup())
