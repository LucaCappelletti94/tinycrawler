from tinycrawler.exceptions import Sleep


def test_sleep():
    try:
        raise Sleep()
        assert False
    except Sleep:
        pass
