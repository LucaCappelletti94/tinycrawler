from tinycrawler.managers import ClientCrawlerManager, ServerCrawlerManager
from httmock import urlmatch, response, HTTMock

default = "232.232.232.111"


@urlmatch(netloc=r'.*\.(org|me)')
def mock_ip_success(*args):
    """Method to mock successfull requests to various ip services."""
    global default
    return response(content=default)


def test_client_crawler_manager():
    with HTTMock(mock_ip_success):
        scm = ServerCrawlerManager(
            "localhost",
            0,
            b"abc",
            useragent="*",
            default_url_timeout=0,
            robots_timeout=0,
            follow_robot_txt=True,
            bloom_filter_capacity=10000)
        scm.start()
        ccm = ClientCrawlerManager(*scm.address, b"abc")
        ccm.connect()
