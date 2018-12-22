"""Test to see if everything is working within ip."""
from tinycrawler.utils import ip
import requests
from httmock import all_requests, response, HTTMock

default = "232.232.232.111"


@all_requests
def mock_ip_success(*args):
    """Method to mock successfull requests to various ip services."""
    global default
    return response(content=default)


@all_requests
def mock_ip_failures(*args):
    """Method to mock unsuccessfull requests to various ip services."""
    raise requests.ConnectionError


def test_ip():
    """Test to see if everything is working within ip."""
    global default
    with HTTMock(mock_ip_success):
        assert default == ip()

    try:
        with HTTMock(mock_ip_failures):
            assert default == ip()
    except requests.RequestException:
        pass
