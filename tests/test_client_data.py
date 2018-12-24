"""Test to see if everything is working within ip."""
from tinycrawler.expirables import ClientData
from httmock import HTTMock
from .utils import mock_ip_success


def test_client_data():
    path = "test_data/expected_client_data_representation.json"
    with HTTMock(mock_ip_success):
        assert ClientData(3) == ClientData(3)
        with open(path, "r") as f:
            assert str(ClientData(0)) == f.read()
