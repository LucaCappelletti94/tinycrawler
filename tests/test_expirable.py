from tinycrawler.expirables.expirable import Expirable
from tinycrawler.exceptions import ExpiredError
from .utils import arguments_test
import json
import numpy as np


def test_expirable_arguments():
    invalid_arguments = {
        "maximum_error_threshold": np.concatenate((
            np.linspace(-10, 0),
            np.linspace(1.1, 10)
        ))
    }
    valid_arguments = {
        "maximum_error_threshold": np.linspace(0.1, 1)
    }

    arguments_test(Expirable, valid_arguments, invalid_arguments)

    assert True


def test_expiration():
    expirable = Expirable(
        maximum_consecutive_errors=3,
        maximum_error_threshold=0.5
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
        maximum_error_threshold=0.5
    )

    for i in range(2):
        expirable.use()
        expirable.used(success=0)

    with open("test_data/expected_expirable_representation.json", "r") as f:
        print(expirable)
        assert str(expirable) == json.load(f)
