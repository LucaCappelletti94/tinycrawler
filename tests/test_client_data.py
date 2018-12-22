"""Test to see if everything is working within ip."""
from tinycrawler.expirables import ClientData
from httmock import all_requests, response, HTTMock
import platform

default = "232.232.232.111"


@all_requests
def mock_ip_success(*args):
    """Method to mock successfull requests to various ip services."""
    global default
    return response(content=default)


def mock_platform(*args)->str:
    """Method to mock calls to platform."""
    return "Mocked platform"


platform.platform = mock_platform


def test_client_data():
    path = "test_data/expected_client_data_representation.json"
    with HTTMock(mock_ip_success):
        assert ClientData(3) == ClientData(3)
        with open(path, "r") as f:
            assert str(ClientData(0)) == f.read()
