from tinycrawler.collections import TypeDict
from ..utils import mock_repr

example_value = "Non devi manducare"


def setup():
    global example_value
    return TypeDict(str, str)


def test_type_dict():
    global example_value
    type_dict = setup()
    type_dict[example_value] = example_value
    assert type_dict[example_value] == example_value

    try:
        type_dict[2] = 6
        assert False
    except AssertionError:
        pass

    try:
        type_dict["hjk"] = 6
        assert False
    except AssertionError:
        pass

    try:
        type_dict.setdefault(3)
        assert False
    except NotImplementedError:
        pass

    try:
        type_dict.get(3)
        assert False
    except NotImplementedError:
        pass

    del type_dict[example_value]
    assert example_value not in type_dict

    try:
        del type_dict[2]
        assert False
    except AssertionError:
        pass

    try:
        2 in type_dict
        assert False
    except AssertionError:
        pass


def test_type_dict_repr():
    mock_repr(setup())
