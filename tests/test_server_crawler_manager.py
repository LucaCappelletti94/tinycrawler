from tinycrawler.managers import ServerCrawlerManager
from tinycrawler.expirables import ClientData
from httmock import all_requests, response, HTTMock

default = "232.232.232.111"


@all_requests
def mock_ip_success(*args):
    """Method to mock successfull requests to various ip services."""
    global default
    return response(content=default)


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
            bloom_filter_capacity=10000)

        scm.handle_client_registration(ClientData(0))
