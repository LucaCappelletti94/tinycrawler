from tinycrawler.utils import Printable
import pytest


def test_printable():
    p = Printable()

    with pytest.raises(NotImplementedError):
        str(p)
