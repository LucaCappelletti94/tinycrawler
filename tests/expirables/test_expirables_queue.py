from tinycrawler.expirables import ExpirablesQueue
from tinycrawler import Domain
from queue import Empty
from .test_domain import setup as domain_setup
from ..commons import mock_repr


def setup():
    q = ExpirablesQueue(Domain)
    q.add(domain_setup())
    return q


def test_expirables_queue():
    try:
        ExpirablesQueue(str)
    except AssertionError:
        pass

    q = setup()
    q.pop()

    try:
        q.pop()
        assert False
    except Empty:
        pass

    domain = domain_setup()

    domain.use()
    domain.used(success=False)

    try:
        q.add(domain)
    except AssertionError:
        pass

    domain = Domain(
        "https://github.com/LucaCappelletti94/tinycrawler")

    unavailable_domain = Domain(
        "https://youtibe.com/LucaCappelletti94/tinycrawler", maximum_usages=1)

    unavailable_domain.use()

    q.add(unavailable_domain)
    q.add(domain)

    assert q.pop() == domain

    try:
        q.pop()
        assert False
    except Empty:
        pass

    unavailable_domain.used(success=True)

    assert q.pop() == unavailable_domain
    q.add(domain)


def test_expirables_queue_repr():
    mock_repr(setup())
