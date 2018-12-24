from httmock import urlmatch, response
import requests
default_ip = "232.232.232.111"

regex = r'\.*(api\.ipify\.org|ident\.me)'


@urlmatch(netloc=regex)
def mock_ip_success(*args):
    """Method to mock successfull requests to various ip services."""
    global default_ip
    return response(content=default_ip)


@urlmatch(netloc=regex)
def mock_ip_failures(*args):
    """Method to mock unsuccessfull requests to various ip services."""
    raise requests.ConnectionError
