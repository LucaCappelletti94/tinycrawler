from tinycrawler.managers import ClientCrawlerManager
from .utils import mock_ip_success, mock_repr
from .test_server_crawler_manager import setup as server_manager_setup
from httmock import HTTMock


def setup():
    with HTTMock(mock_ip_success):
        scm = server_manager_setup()
        ccm = ClientCrawlerManager(*scm.address, b"abc")
        ccm.connect()
        return ccm


def test_client_crawler_manager():
    setup()


def test_client_crawler_manager_repr():
    mock_repr(setup())
