from tinycrawler.data import Urls
from tinycrawler import Url
from queue import Empty
from ..commons import mock_robots, mock_sensitive_robots, build_default_url, mock_repr
from httpretty import httprettified
import pytest


@httprettified
def test_urls():
    mock_robots()
    urls = Urls(
        bloom_filter_capacity=10000,
        follow_robot_txt=True,
        useragent="*",
        default_url_timeout=1,
        robots_timeout=0,
        url_maximum_consecutive_errors=3,
        url_maximum_error_rate=0.5,
    )

    urls.add(build_default_url("/error"))

    # Failure 'cos of robots can download
    with pytest.raises(Empty):
        urls.pop()

    url = build_default_url("/homepage")
    urls.add(url)
    assert urls.pop().url == url

    # Failure 'cos of bloom filter
    url = build_default_url("/homepage")
    urls.add(url)
    with pytest.raises(Empty):
        urls.pop()

    # Failure 'cos of timeout reset
    url = Url(build_default_url("/new"))
    url.use()
    urls.add(url)
    with pytest.raises(Empty):
        urls.pop()

    # Extraction of last inserted as it is ready
    url1 = Url(build_default_url("/1"))
    url1.use()
    url2 = Url(build_default_url("/sensitive"))
    url3 = Url(build_default_url("/3"))
    urls.add(url1)
    urls.add(url2)
    urls.add(url3)

    mock_sensitive_robots()

    assert urls.pop() == url3
    mock_repr(urls)
