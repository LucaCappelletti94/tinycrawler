from tinycrawler.collections import Sporadic
from tinycrawler.exceptions import UnavailableError
from .utils import double_arguments_test
import numpy as np


def test_sporadic_arguments():
    invalid_arguments = {
        "used_timeout": np.linspace(-10, 0, endpoint=False),
        "use_timeout": np.linspace(-10, 0, endpoint=False)
    }
    valid_arguments = {
        "used_timeout": np.linspace(0, 10),
        "use_timeout": np.linspace(0, 10)
    }

    double_arguments_test(Sporadic, valid_arguments, invalid_arguments)

    assert True


def test_sporadic():
    sporadic = Sporadic(
        used_timeout=1,
        use_timeout=1
    )

    sporadic.use()
    try:
        sporadic.use()
        assert False
    except UnavailableError:
        pass

    sporadic.used()
    try:
        sporadic.use()
        assert False
    except UnavailableError:
        pass

    sporadic = Sporadic()

    sporadic.use()
    sporadic.use()
    sporadic.used()
    sporadic.used()

    assert True
