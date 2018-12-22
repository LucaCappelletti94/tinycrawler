"""Test to verify that class CLients has everything in order."""
from tinycrawler.data import Clients
from tinycrawler import IllegalArgumentError
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


def test_clients():
    with HTTMock(mock_ip_success):
        clients = Clients()
        client = ClientData(clients.get_new_client_id())
        client2 = ClientData(clients.get_new_client_id())
        clients.register(client)
        try:
            clients.register(client)
            assert False
        except IllegalArgumentError:
            pass

        assert client in clients
        assert client2 not in clients

        with open("test_data/expected_clients_representation.json", "r") as f:
            assert str(clients) == f.read()
