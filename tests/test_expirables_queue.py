from tinycrawler.expirables import ExpirablesQueue
from tinycrawler import Domain, IllegalArgumentError
from queue import Empty


def test_expirables_queue():
    try:
        ExpirablesQueue(str)
        assert False
    except IllegalArgumentError:
        pass

    q = ExpirablesQueue(Domain)

    try:
        q.pop()
        assert False
    except Empty:
        pass

    domain = Domain("https://github.com/LucaCappelletti94/tinycrawler", maximum_consecutive_errors=1,
                    maximum_error_rate=0.5)

    domain.use()
    domain.used(success=False)

    try:
        q.add(domain)
        assert False
    except IllegalArgumentError:
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

    with open("test_data/expected_espirables_queue_representation.json", "r") as f:
        assert str(q) == f.read()
