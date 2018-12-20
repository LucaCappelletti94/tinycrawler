from tinycrawler.data import Urls
from tinycrawler import Url
from queue import Empty
from httpretty import HTTPretty, httprettified


@httprettified
def test_urls():
    with open("test_data/robots.txt", "r") as f:
        HTTPretty.register_uri(
            HTTPretty.GET,
            "http://www.totally.fake.example.com/robots.txt",
            body=f.read(),
            content_type="text/plain"
        )

    urls = Urls(
        capacity=10000,
        follow_robot_txt=True,
        useragent="*",
        default_url_timeout=1,
        robots_timeout=10
    )

    urls.add(
        set([Url("http://www.totally.fake.example.com/error", use_timeout=5)]))

    # Failure 'cos of robots can download
    try:
        urls.pop()
        assert False
    except Empty:
        pass

    url = Url("http://www.totally.fake.example.com/homepage", use_timeout=5)
    urls.add(set([url]))
    assert urls.pop() == url

    # Failure 'cos of bloom filter
    url = Url("http://www.totally.fake.example.com/homepage", use_timeout=5)
    urls.add(set([url]))
    try:
        urls.pop()
        assert False
    except Empty:
        pass

    # Failure 'cos of timeout reset
    url = Url("http://www.totally.fake.example.com/new", use_timeout=5)
    url.use()
    urls.add(set([url]))
    try:
        urls.pop()
        assert False
    except Empty:
        pass

    # Extraction of last inserted as it is ready
    url1 = Url("http://www.totally.fake.example.com/1", use_timeout=5)
    url1.use()
    url2 = Url("http://www.totally.fake.example.com/2", use_timeout=5)
    url2.use()
    url3 = Url("http://www.totally.fake.example.com/3", use_timeout=5)
    urls.add(set([url1, url2, url3]))

    assert urls.pop() == url3

    with open("test_data/expected_urls_representation.json", "r") as f:
        assert str(urls) == f.read()
