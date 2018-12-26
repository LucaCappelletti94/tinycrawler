from tinycrawler.expirables import ExpirableRobotFileParser
from tinycrawler.expirables.web.expirable_robot_file_parser import RobotFileParser
from tinycrawler import Domain
from httpretty import HTTPretty, httprettified

backup = RobotFileParser.read


def create_robots(follow, timeout)->ExpirableRobotFileParser:
    domain = Domain("http://www.totally.fake.example.com")
    return ExpirableRobotFileParser(domain, "tinycrawler", follow, timeout, use_timeout=10)


@httprettified
def test_expirable_robots_file_parser():
    with open("test_data/robots.txt", "r") as f:
        HTTPretty.register_uri(
            HTTPretty.GET,
            "http://www.totally.fake.example.com/robots.txt",
            body=f.read(),
            content_type="text/plain"
        )

    robots = create_robots(True, 0)

    valid = [
        "http://www.totally.fake.example.com/homepage"
    ]
    invalid = [
        "http://www.totally.fake.example.com/error",
        "http://www.totally.fake.example.com/Locale"
    ]

    for url in valid:
        assert robots.can_download(url)

    for url in invalid:
        assert not robots.can_download(url)

    assert robots.timeout == 5
    assert robots._crawl_delay_ == 2
    assert robots._request_rate_delay_ == 5

    with open("test_data/expected_robots_representation.json", "r") as f:
        assert str(robots) == f.read()


@httprettified
def test_unfollowed_expirable_robots_file_parser():
    with open("test_data/robots.txt", "r") as f:
        HTTPretty.register_uri(
            HTTPretty.GET,
            "http://www.totally.fake.example.com/robots.txt",
            body=f.read(),
            content_type="text/plain"
        )

    robots = create_robots(False, 1)

    valid = [
        "http://www.totally.fake.example.com/homepage",
        "http://www.totally.fake.example.com/error",
        "http://www.totally.fake.example.com/Locale"
    ]

    for url in valid:
        assert robots.can_download(url)

    assert robots.timeout == 1
    assert robots._crawl_delay_ == 0
    assert robots._request_rate_delay_ == 0

    with open("test_data/unfollowed_expected_robots_representation.json", "r") as f:
        assert str(robots) == f.read()
