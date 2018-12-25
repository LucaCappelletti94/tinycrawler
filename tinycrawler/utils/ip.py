"""Return current machine public ip."""
from requests import get, RequestException


def get_ip()->str:
    """Return current machine public ip."""
    services = [
        "https://api.ipify.org",
        "https://ident.me"
    ]
    for service in services:
        try:
            return get(service).text
        except RequestException:
            pass
    raise RequestException()
