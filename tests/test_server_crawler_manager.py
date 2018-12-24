from tinycrawler.managers import ServerCrawlerManager
from tinycrawler.expirables import ClientData
from .utils import mock_ip_success
from httmock import HTTMock


def test_server_crawler_manager():
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

        scm.handle_client_registration(ClientData(0))

        scm.start()
