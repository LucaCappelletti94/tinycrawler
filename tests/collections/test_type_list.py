from tinycrawler.collections import TypeList
from ..commons import mock_repr
import pytest


def setup():
    type_list = TypeList(str)
    type_list.append("Lo kebabbo")
    return type_list


def test_type_list():
    type_list = setup()

    with pytest.raises(AssertionError):
        type_list.append(2)

    with pytest.raises(AssertionError):
        type_list.prepend(2)

    with pytest.raises(NotImplementedError):
        type_list[2] = 3


def test_type_list_repr():
    mock_repr(setup())
