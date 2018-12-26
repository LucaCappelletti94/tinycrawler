from tinycrawler.data import Urls
from tinycrawler import Url
from queue import Empty
from ..commons import mock_robots, mock_sensitive_robots, build_default_url, build_repr
from httpretty import httprettified, reset


@httprettified
def test_urls():

    mock_robots()

    urls = Urls(
        bloom_filter_capacity=10000,
        follow_robot_txt=True,
        useragent="*",
        default_url_timeout=1,
        robots_timeout=0
    )

    urls.add(
        set([Url(build_default_url("/error"), use_timeout=5)]))

    # Failure 'cos of robots can download
    try:
        urls.pop()
        assert False
    except Empty:
        pass

    url = Url(build_default_url("/homepage"), use_timeout=5)
    urls.add(set([url]))
    assert urls.pop() == url

    # Failure 'cos of bloom filter
    url = Url(build_default_url("/homepage"), use_timeout=5)
    urls.add(set([url]))
    try:
        urls.pop()
        assert False
    except Empty:
        pass

    # Failure 'cos of timeout reset
    url = Url(build_default_url("/new"), use_timeout=5)
    url.use()
    urls.add(set([url]))
    try:
        urls.pop()
        assert False
    except Empty:
        pass

    # Extraction of last inserted as it is ready
    url1 = Url(build_default_url("/1"), use_timeout=2)
    url1.use()
    url2 = Url(build_default_url("/sensitive"), use_timeout=5)
    url3 = Url(build_default_url("/3"), use_timeout=5)
    urls.add([url1, url3, url2])

    reset()

    mock_sensitive_robots()

    assert urls.pop() == url3

    with open("test_data/expected_urls_representation.json", "r") as f:
        assert str(urls) == f.read()
