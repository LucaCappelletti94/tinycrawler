from tinycrawler.collections import TypeList
from ..utils import mock_repr


def setup():
    type_list = TypeList(str)
    type_list.append("Lo kebabbo")
    return type_list


def test_type_list():
    type_list = setup()

    try:
        type_list.append(2)
        assert False
    except AssertionError:
        pass

    try:
        type_list.prepend(2)
        assert False
    except AssertionError:
        pass

    try:
        type_list[2] = 3
        assert False
    except NotImplementedError:
        pass


def test_type_list_repr():
    mock_repr(setup())
