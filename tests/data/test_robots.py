from tinycrawler.data import Robots
from tinycrawler import Url
from httpretty import httprettified
from ..commons import mock_repr, mock_robots, build_repr


def setup():
    mock_robots()
    return Robots(
        follow_robot_txt=True,
        useragent="*",
        default_url_timeout=1,
        robots_timeout=10
    )


@httprettified
def test_robots():

    valid = [
        "http://www.totallyfakeexample.com/homepage"
    ]
    invalid = [
        "http://www.totallyfakeexample.com/error",
        "http://www.totallyfakeexample.com/Locale"
    ]

    robots = setup()

    for url in valid + invalid:
        assert robots.get_timeout(Url(url).domain) == 5

    for url in valid:
        assert robots.can_download(Url(url))

    for url in invalid:
        assert not robots.can_download(Url(url))

    build_repr(robots)
    mock_repr(robots)
