from tinycrawler.expirables import CircularExpirablesQueuesDomainDict
from tinycrawler import Url, Domain
from queue import Empty


def test_circular_expirables_list_domain_dict():
    q = CircularExpirablesQueuesDomainDict()

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
