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

    try:
        urls.pop()
    except Empty:
        pass

    url = Url("http://www.totally.fake.example.com/homepage", use_timeout=5)
    urls.add(set([url]))
    assert urls.pop() == url

    timeout_url = Url(
        "http://www.totally.fake.example.com/homepage", use_timeout=1)
    urls.add(set([timeout_url]))
    try:
        urls.pop()
    except Empty:
        pass

    urls.add(set([url]))

    # The following should fail for the bloom filter
    try:
        urls.pop()
    except Empty:
        pass

    url2 = Url("http://www.totally.fake.example.com/testing", use_timeout=5)
    urls.add(set([
        Url("http://www.totally.fake.example.com/test1", use_timeout=1),
        url2
    ]))

    assert urls.pop() == url2

    print(urls)
