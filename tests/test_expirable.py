from tinycrawler.expirables.expirable import Expirable
from tinycrawler import ExpiredError
from .utils import double_arguments_test
import numpy as np


def test_expirable_arguments():
    invalid_maximum_rate = {
        "maximum_error_rate": np.concatenate((
            np.linspace(-10, 0),
            np.linspace(1.1, 10)
        )).tolist()
    }
    corner_maximum_rate = {
        "maximum_error_rate": [1.0]
    }
    corner_maximum_consecutive_errors = {
        "maximum_consecutive_errors": [-1]
    }
    valid_maximum_rate = {
        "maximum_error_rate": np.linspace(0.1, 1, endpoint=False).tolist()
    }
    invalid_maximum_consecutive_errors = {
        "maximum_consecutive_errors": np.arange(-10, -1).tolist()
    }
    valid_maximum_consecutive_errors = {
        "maximum_consecutive_errors": np.arange(0, 10).tolist()
    }
    invalid_arguments = [
        invalid_maximum_rate,
        invalid_maximum_consecutive_errors,
        valid_maximum_consecutive_errors,
        valid_maximum_rate,
        {
            **invalid_maximum_rate,
            **valid_maximum_consecutive_errors
        },
        {
            **valid_maximum_rate,
            **invalid_maximum_consecutive_errors
        },
        {
            **corner_maximum_rate,
            **valid_maximum_consecutive_errors
        },
        {
            **corner_maximum_consecutive_errors,
            **valid_maximum_rate
        }
    ]
    valid_arguments = [
        {
            **valid_maximum_rate,
            **valid_maximum_consecutive_errors
        },
        corner_maximum_rate,
        corner_maximum_consecutive_errors,
        {}
    ]

    double_arguments_test(Expirable, valid_arguments, invalid_arguments)

    assert True


def test_expiration():
    expirable = Expirable(
        maximum_consecutive_errors=3,
        maximum_error_rate=0.5
    )

    for i in range(2):
        expirable.use()
        expirable.used(success=0)

    expirable.use()
    expirable.used(success=1)

    for i in range(3):
        expirable.use()
        expirable.used(success=0)

    try:
        expirable.use()
        assert False
    except ExpiredError:
        assert True


def test_expiration_representation():
    expirable = Expirable(
        maximum_consecutive_errors=3,
        maximum_error_rate=0.5
    )

    for i in range(2):
        expirable.use()
        expirable.used(success=0)

    print(expirable)

    with open("test_data/expected_expirable_representation.json", "r") as f:
        assert str(expirable) == f.read()
