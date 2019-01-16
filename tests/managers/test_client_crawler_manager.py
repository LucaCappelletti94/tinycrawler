from tinycrawler.managers import ClientCrawlerManager
from ..commons import mock_ip_success, mock_repr
from .test_server_crawler_manager import setup as server_manager_setup
from httmock import HTTMock


def setup()->ClientCrawlerManager:
    with HTTMock(mock_ip_success):
        scm = server_manager_setup()
        ccm = ClientCrawlerManager(*scm.address, b"abc")
        ccm.connect()
        return ccm


def test_client_crawler_manager():
    ccm = setup()
    assert ccm.end_event
    assert ccm.urls
    assert ccm.proxies
    assert ccm.clients
    assert ccm.client
    assert ccm.responses
    assert ccm.downloader_tasks
    assert ccm.parser_tasks
    assert ccm.logger
    assert ccm.completed_downloader_tasks
    assert ccm.completed_parser_tasks


def test_client_crawler_manager_repr():
    mock_repr(setup())
