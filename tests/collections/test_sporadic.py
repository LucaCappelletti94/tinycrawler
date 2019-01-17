from tinycrawler.collections import Sporadic
from ..commons import double_arguments_test, mock_repr
import numpy as np
import pytest


def sporadic_setup():
    return Sporadic(
        used_timeout=1,
        use_timeout=1
    )


def test_sporadic_arguments():
    valid_use = {
        "use_timeout": np.linspace(0, 10)
    }
    invalid_use = {
        "use_timeout": np.linspace(-10, 0, endpoint=False)
    }
    valid_used = {
        "used_timeout": np.linspace(0, 10)
    }
    invalid_used = {
        "used_timeout": np.linspace(-10, 0, endpoint=False)
    }

    invalid_arguments = [
        {
            **valid_use,
            **invalid_used
        },
        {
            **valid_use,
            **invalid_used
        },
        {
            **invalid_use,
            **invalid_used
        }
    ]
    valid_arguments = [
        valid_use,
        valid_used,
        {
            **valid_use,
            **valid_used
        }
    ]

    double_arguments_test(Sporadic, valid_arguments, invalid_arguments)

    assert True


def test_sporadic():
    sporadic = sporadic_setup()

    sporadic.use()
    with pytest.raises(AssertionError):
        sporadic.use()

    sporadic.used()
    with pytest.raises(AssertionError):
        sporadic.use()

    sporadic = Sporadic()

    sporadic.use()
    sporadic.use()
    sporadic.used()
    sporadic.used()

    assert True


def test_sporadic_repr():
    mock_repr(sporadic_setup())
