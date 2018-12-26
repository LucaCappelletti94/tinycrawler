from tinycrawler.expirables.sporadic_sequential_expirable import SporadicSequentialExpirable
import numpy as np
from ..commons import double_arguments_test


def test_sporadic_sequential_expirable_arguments():
    valid_arguments = [
        {},
        {
            "maximum_usages": np.arange(2).tolist(),
            "used_timeout": np.linspace(0, 10, num=5).tolist(),
            "use_timeout": np.linspace(0, 10, num=5).tolist(),
            "maximum_consecutive_errors": np.arange(0, 2).tolist(),
            "maximum_error_rate": np.linspace(0.1, 1, endpoint=False, num=5).tolist()
        }
    ]

    double_arguments_test(SporadicSequentialExpirable,
                          valid_arguments, [])

    assert True


def test_sporadic_sequential_expirable():
    s = SporadicSequentialExpirable(
        maximum_usages=3,
        maximum_consecutive_errors=2,
        maximum_error_rate=0.7
    )

    # This will increase parallel usages by one
    s.use()
    s.use()
    s.use()
    # Now the error count will raise to 1
    try:
        s.use()
        assert False
    except AssertionError:
        pass

    assert True


def test_sporadic_sequential_expirable_representation():
    s = SporadicSequentialExpirable(
        maximum_usages=1,
        maximum_consecutive_errors=2,
        maximum_error_rate=0.7
    )

    for i in range(2):
        s.use()
        s.used(success=0)

    with open("test_data/expected_sporadic_sequential_expirable_representation.json", "r") as f:
        assert str(s) == f.read()
