from typing import Dict


class ProxyData(dict):
    PROTOCOLS = {
        "http": "http",
        "https": "https",
        "socks4": "https",
        "socks5": "https"
    }

    ADDRESS = "{protocol}://{ip}:{port}"

    def __init__(self, data: Dict):
        super(ProxyData, self).__init__(
            {protocol:  ProxyData.ADDRESS.format(
                protocol=protocol,
                ip=data["ip"],
                port=data["port"]
            ) for key, protocol in ProxyData.PROTOCOLS.items() if data["support"][key]}
        )
