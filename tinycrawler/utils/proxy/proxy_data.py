from typing import Dict
from ..output import Printable


class ProxyData(Printable):
    PROTOCOLS = {
        "http": "http",
        "https": "https",
        "socks4": "https",
        "socks5": "https"
    }

    ADDRESS = "{protocol}://{ip}:{port}"

    def __init__(self, **kwargs):
        data = kwargs.get("data", None)
        self._data = {protocol:  ProxyData.ADDRESS.format(
            protocol=protocol,
            ip=data["ip"],
            port=data["port"]
        ) for key, protocol in ProxyData.PROTOCOLS.items() if data["support"][key]} if data else None
        self._ip = data["ip"] if data else kwargs.get("ip")

    @property
    def ip(self):
        return self._ip

    @property
    def data(self):
        return self._data

    def ___repr___(self):
        return {
            "data": self.data,
            "ip": self.ip
        }
