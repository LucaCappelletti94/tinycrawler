"""Create a client side object for managing the crawler data."""
from .crawler_manager import CrawlerManager
from ..expirables import ClientData
from typing import Dict


class ClientCrawlerManager(CrawlerManager):
    """Create a client side object for managing the crawler data."""

    def __init__(self, host: str, port: int, authkey: str):
        """Create a client side object for managing the crawler data."""
        super(ClientCrawlerManager, self).__init__(
            host,
            port,
            authkey
        )
        for endpoint in self.endpoints:
            self.register(endpoint)

    def connect(self):
        """Handle connection to the server manager."""
        super(ClientCrawlerManager, self).connect()
        self._client = ClientData(self.get_clients().get_new_client_id())
        self.register_client(self._client)

    def ___repr___(self)->Dict:
        return {
            **super(ClientCrawlerManager, self).___repr___(),
            "client": self._client.___repr___()
        }
