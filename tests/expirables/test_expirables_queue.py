from tinycrawler.expirables import ExpirablesQueue
from tinycrawler import Domain
from queue import Empty
from .test_domain import setup as domain_setup
from ..commons import mock_repr
import pytest


def setup(classtype=None):
    return ExpirablesQueue(classtype or Domain)


def test_expirables_queue():
    with pytest.raises(AssertionError):
        ExpirablesQueue(str)

    q = setup()

    with pytest.raises(Empty):
        q.pop()

    domain = domain_setup()

    domain.use()
    domain.used(success=False)

    with pytest.raises(AssertionError):
        q.add(domain)

    domain = Domain(
        "https://github.com/LucaCappelletti94/tinycrawler")

    unavailable_domain = Domain(
        "https://youtibe.com/LucaCappelletti94/tinycrawler", maximum_usages=1)

    unavailable_domain.use()

    q.add(unavailable_domain)
    q.add(domain)

    assert q.pop() == domain

    with pytest.raises(Empty):
        q.pop()

    unavailable_domain.used(success=True)

    assert q.pop() == unavailable_domain
    q.add(domain)


def test_expirables_queue_repr():
    mock_repr(setup())
