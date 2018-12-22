from ..expirables import DomainsDict, ClientData, ExpirablesQueue
from ..utils import Printable
from ..exceptions import IllegalArgumentError
from multiprocessing import Lock


class Clients(Printable):
    def __init__(self):
        self._client_counter = 0
        self._new_id_lock = Lock()
        self._clients = DomainsDict(ExpirablesQueue)

    def get_new_client_id(self)->int:
        """Return an unique client id."""
        with self._new_id_lock:
            self._client_counter += 1
            return self._client_counter

    def register(self, client_data: ClientData):
        if client_data.ip not in self._clients:
            self._clients[client_data.ip] = ExpirablesQueue(ClientData)
        if client_data in self:
            raise IllegalArgumentError("Given client is already registered.")
        self._clients[client_data.ip].append(client_data)

    def __contains__(self, client_data: ClientData)->bool:
        return client_data.ip in self._clients and client_data in self._clients[client_data.ip]

    def ___repr___(self):
        """Return a dictionary representation of object."""
        return {
            "clients": self._clients.___repr___()
        }
