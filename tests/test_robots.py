from tinycrawler.data import Robots
from tinycrawler import Url
from httpretty import HTTPretty, httprettified


@httprettified
def test_robots():
    with open("test_data/robots.txt", "r") as f:
        HTTPretty.register_uri(
            HTTPretty.GET,
            "http://www.totallyfakeexample.com/robots.txt",
            body=f.read(),
            content_type="text/plain"
        )

    valid = [
        "http://www.totallyfakeexample.com/homepage"
    ]
    invalid = [
        "http://www.totallyfakeexample.com/error",
        "http://www.totallyfakeexample.com/Locale"
    ]

    robots = Robots(
        follow_robot_txt=True,
        useragent="*",
        default_url_timeout=1,
        robots_timeout=10
    )

    for url in valid + invalid:
        assert robots.get_timeout(Url(url).domain) == 5

    for url in valid:
        assert robots.can_download(Url(url))

    for url in invalid:
        assert not robots.can_download(Url(url))

    with open("test_data/expected_robots_data_representation.json", "r") as f:
        assert str(robots) == f.read()
