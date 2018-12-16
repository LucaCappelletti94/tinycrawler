from tinycrawler.collections import Sequential
from tinycrawler import NotInUseError, UnavailableError


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
    except UnavailableError:
        pass

    sequential.used()

    assert True
