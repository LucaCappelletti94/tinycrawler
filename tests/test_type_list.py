from tinycrawler.collections import TypeList
from tinycrawler import IllegalArgumentError


def test_type_list():
    l = TypeList(str)

    try:
        l.append(2)
        assert False
    except IllegalArgumentError:
        pass

    try:
        l.prepend(2)
        assert False
    except IllegalArgumentError:
        pass

    try:
        l[2] = 3
        assert False
    except NotImplementedError:
        pass

    l.append("ciao")
