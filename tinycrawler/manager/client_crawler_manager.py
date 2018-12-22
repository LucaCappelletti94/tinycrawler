from .crawler_manager import CrawlerManager
from ..expirables import ClientData


class ClientCrawlerManager(CrawlerManager):

    def __init__(self, host: str, port: int, authkey: str):
        super(ClientCrawlerManager, self).__init__(
            host,
            port,
            authkey
        )
        for service in dir(CrawlerManager):
            if callable(getattr(CrawlerManager, service)) and service.startswith("get_"):
                self.register(service)

    def connect(self):
        """Handle connection to the server manager."""
        super(ClientCrawlerManager, self).connect()
        self._client = ClientData(self.get_client_id())
