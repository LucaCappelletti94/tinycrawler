from tinycrawler.collections import Sequential
from ..commons import mock_repr
import pytest


def setup():
    return Sequential(maximum_usages=1)


def test_sequential():
    sequential = setup()
    with pytest.raises(AssertionError):
        sequential.used()
    sequential.use()
    with pytest.raises(AssertionError):
        sequential.use()

    sequential.used()


def test_sequential_repr():
    mock_repr(setup())
