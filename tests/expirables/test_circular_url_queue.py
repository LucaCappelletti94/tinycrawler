from tinycrawler.expirables import CircularUrlQueue
from tinycrawler import Url
from queue import Empty
from ..commons import mock_repr
from .test_url import url_setup
import pytest


def circular_setup():
    q = CircularUrlQueue()
    q.add(url_setup())
    return q


def test_circular_url_queue():
    q = circular_setup()
    q.pop()

    with pytest.raises(Empty):
        q.pop()

    with pytest.raises(Empty):
        CircularUrlQueue().pop()

    url = Url(
        "https://docs.python.org/3/tutorial/datastructures.html",
        maximum_consecutive_errors=1,
        maximum_error_rate=0.5
    )
    q.add(url)
    assert q.pop() == url

    url.use()

    q.add(url)

    with pytest.raises(Empty):
        q.pop()


def test_circular_url_queue_repr():
    mock_repr(circular_setup())
