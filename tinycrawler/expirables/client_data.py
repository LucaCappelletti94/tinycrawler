"""Class to represent a client's important characteristics."""
from .sporadic_expirable import SporadicExpirable
from .web import Domain
import platform
from ..utils import get_ip


class ClientData(SporadicExpirable):
    """Create a new client data object."""

    def __init__(self, client_id: int, **kwargs):
        """Create a new client data object.
            client_id:int, the client unique id.
        """
        super(ClientData, self).__init__(**kwargs)
        self._client_id = client_id
        self._ip = Domain(get_ip())
        self._platform = platform.platform()

    @property
    def client_id(self)->int:
        """Return int identifying uniquely current client."""
        return self._client_id

    @property
    def platform(self)->str:
        """Return string summing up client's system."""
        return self._platform

    @property
    def ip(self)->Domain:
        """Return client public ip."""
        return self._ip

    def __eq__(self, other)->bool:
        """Determines if given object is same client_data object."""
        return other is not None and isinstance(other, ClientData) and other.client_id == self.client_id and other.ip == self.ip and self.platform == other.platform

    def ___repr___(self):
        """Return a dictionary representation of object."""
        return {
            **super(ClientData, self).___repr___(),
            **{
                "ip": self.ip.___repr___(),
                "platform": self.platform,
                "client_id": self.client_id
            }}
