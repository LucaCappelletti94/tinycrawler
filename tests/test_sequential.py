from tinycrawler.collections import Sequential
from tinycrawler.exceptions import NotInUseError, InUseError


def test_sequential():
    sequential = Sequential(maximum_usages=1)
    try:
        sequential.used()
        assert False
    except NotInUseError:
        pass
    sequential.use()
    try:
        sequential.use()
        assert False
    except InUseError:
        pass

    sequential.used()

    assert True
