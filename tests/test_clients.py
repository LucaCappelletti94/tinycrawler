"""Test to verify that class CLients has everything in order."""
from tinycrawler.data import Clients
from tinycrawler import IllegalArgumentError
from tinycrawler.expirables import ClientData
from .utils import mock_ip_success
from httmock import HTTMock


def test_clients():
    with HTTMock(mock_ip_success):
        clients = Clients()
        client = ClientData(clients.get_new_client_id())
        client2 = ClientData(clients.get_new_client_id())
        assert clients.is_new_ip(client.ip)
        clients.register(client)
        try:
            clients.register(client)
            assert False
        except IllegalArgumentError:
            pass

        assert not clients.is_new_ip(client.ip)

        assert client in clients
        assert client2 not in clients

        with open("test_data/expected_clients_representation.json", "r") as f:
            assert str(clients) == f.read()
