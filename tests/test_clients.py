"""Test to verify that class CLients has everything in order."""
from tinycrawler.data import Clients
from tinycrawler.expirables import ClientData
from .commons import mock_ip_success, mock_repr
from httmock import HTTMock


def setup():
    with HTTMock(mock_ip_success):
        clients = Clients()
        clients.register(ClientData(clients.get_new_client_id()))
        return clients


def test_clients():
    clients = setup()
    with HTTMock(mock_ip_success):
        client2 = ClientData(clients.get_new_client_id())
    assert not clients.is_new_ip(client2.ip)
    assert client2 not in clients


def test_clients_repr():
    mock_repr(setup())
