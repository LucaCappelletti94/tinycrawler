from tinycrawler.utils import Printable


def test_printable():
    p = Printable()

    try:
        str(p)
        assert False
    except NotImplementedError:
        pass
