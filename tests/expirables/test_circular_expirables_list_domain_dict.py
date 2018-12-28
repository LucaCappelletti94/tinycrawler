from tinycrawler.expirables import CircularExpirablesQueuesDomainDict
from tinycrawler import Url
from queue import Empty
from ..commons import mock_repr
from .test_url import setup as url_setup
import pytest


def setup():
    q = CircularExpirablesQueuesDomainDict()
    q.add(url_setup())
    return q


def test_circular_expirables_list_domain_dict():
    q = setup()
    q.pop()

    with pytest.raises(Empty):
        q.pop()

    with pytest.raises(Empty):
        CircularExpirablesQueuesDomainDict().pop()

    url = Url(
        "https://docs.python.org/3/tutorial/datastructures.html", use_timeout=500)
    q.add(url)
    assert q.pop() == url

    url.use()

    q.add(url)

    with pytest.raises(Empty):
        q.pop()


def test_circular_expirables_list_domain_dict_repr():
    mock_repr(setup())
