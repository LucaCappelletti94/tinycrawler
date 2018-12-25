from tinycrawler.managers import ServerCrawlerManager
from .utils import mock_ip_success, mock_repr
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
            follow_robot_txt=True,
            log_filename="logs/crawler.log",
            bloom_filter_capacity=10000)
        scm.start()
        return scm


def test_server_crawler_manager():
    setup()


def test_server_crawler_manager_repr():
    mock_repr(setup())
