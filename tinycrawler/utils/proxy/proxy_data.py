"""Create a wrapper for the data required to make a Proxy object function."""
from typing import Dict
from ..output import Printable


class ProxyData(Printable):
    """Create a wrapper for the data required to make a Proxy object function."""
    PROTOCOLS = {
        "http": "http",
        "https": "https",
        "socks4": "https",
        "socks5": "https"
    }

    ADDRESS = "{protocol}://{ip}:{port}"

    def __init__(self, **kwargs):
        """Create a wrapper for the data required to make a Proxy object function."""
        data = kwargs.get("data", None)
        self._data = {protocol:  ProxyData.ADDRESS.format(
            protocol=protocol,
            ip=data["ip"],
            port=data["port"]
        ) for key, protocol in ProxyData.PROTOCOLS.items() if data["support"][key]} if data else None
        self._ip = data["ip"] if data else kwargs.get("ip")

    @property
    def ip(self):
        """Return ip of proxy."""
        return self._ip

    @property
    def data(self):
        """Return data of proxy required for requests get connection."""
        return self._data

    def ___repr___(self)->Dict:
        """Return a dictionary representing the object."""
        return {
            "data": self.data,
            "ip": self.ip
        }
