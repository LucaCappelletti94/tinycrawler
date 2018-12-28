from tinycrawler.managers import ServerCrawlerManager
from ..commons import mock_ip_success, mock_repr
from httmock import HTTMock


def setup():
    with HTTMock(mock_ip_success):
        scm = ServerCrawlerManager(
            "",
            0,
            b"abc",
            useragent="*",
            default_url_timeout=0,
            robots_timeout=0,
            follow_robot_txt=False,
            log_filename="logs/crawler.log",
            url_maximum_consecutive_errors=3,
            url_maximum_error_rate=0.5,
            bloom_filter_capacity=10000)
        scm.start()
        return scm


def test_server_crawler_manager():
    setup()


def test_server_crawler_manager_repr():
    mock_repr(setup())
