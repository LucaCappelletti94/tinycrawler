from tinycrawler.collections import TypeDict
from ..commons import mock_repr
import pytest
example_value = "Non devi manducare"


def setup():
    global example_value
    return TypeDict(str, str)


def test_type_dict():
    global example_value
    type_dict = setup()
    type_dict[example_value] = example_value
    assert type_dict[example_value] == example_value

    with pytest.raises(AssertionError):
        type_dict[2] = 6

    with pytest.raises(AssertionError):
        type_dict["hjk"] = 6

    with pytest.raises(NotImplementedError):
        type_dict.setdefault(3)

    with pytest.raises(NotImplementedError):
        type_dict.get(3)

    del type_dict[example_value]
    assert example_value not in type_dict

    with pytest.raises(AssertionError):
        del type_dict[2]

    with pytest.raises(AssertionError):
        2 in type_dict


def test_type_dict_repr():
    mock_repr(setup())
