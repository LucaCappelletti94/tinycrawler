"""Test to see if everything is working within ip."""
from tinycrawler.expirables import ClientData
from httmock import HTTMock
from ..commons import mock_ip_success, mock_repr


def client_data_setup():
    with HTTMock(mock_ip_success):
        return ClientData(3)


def test_client_data():
    assert client_data_setup() == client_data_setup()


def test_client_data_repr():
    mock_repr(client_data_setup())
