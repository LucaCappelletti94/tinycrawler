from tinycrawler.expirables import CircularExpirablesQueuesDomainDict
from tinycrawler import Url
from queue import Empty
from .utils import mock_repr


def setup():
    q = CircularExpirablesQueuesDomainDict()
    url = Url("https://docs.python.org/3/tutorial/datastructures.html")
    q.add(url)
    return q


def test_circular_expirables_list_domain_dict():
    q = setup()

    q.pop()

    try:
        q.pop()
        assert False
    except Empty:
        pass

    url = Url("https://docs.python.org/3/tutorial/datastructures.html")
    q.add(url)
    assert q.pop() == url

    try:
        q.pop()
        assert False
    except Empty:
        pass


def test_circular_expirables_list_domain_dict_repr():
    mock_repr(setup())
