from tinycrawler.expirables import ExpirableRobotFileParser
from tinycrawler.expirables.web.expirable_robot_file_parser import RobotFileParser
from tinycrawler import Domain
from httpretty import HTTPretty, httprettified

backup = RobotFileParser.read


def create_robots()->ExpirableRobotFileParser:
    domain = Domain("http://www.totally.fake.example.com")
    return ExpirableRobotFileParser(domain, "tinycrawler", use_timeout=10)


@httprettified
def test_expirable_robots_file_parser():
    with open("test_data/robots.txt", "r") as f:
        HTTPretty.register_uri(
            HTTPretty.GET,
            "http://www.totally.fake.example.com/robots.txt",
            body=f.read(),
            content_type="text/plain"
        )

    robots = create_robots()

    valid = [
        "http://www.totally.fake.example.com/homepage"
    ]
    invalid = [
        "http://www.totally.fake.example.com/error"
        "http://www.totally.fake.example.com/Locale"
    ]

    for url in valid:
        assert robots.can_fetch(url)

    for url in invalid:
        assert not robots.can_fetch(url)

    assert robots.timeout == 5
    assert robots._crawl_delay_ == 2
    assert robots._request_rate_delay_ == 5

    with open("test_data/expected_robots_representation.json", "r") as f:
        str(robots) == f.read()
