"""Test to see if everything is working within ip."""
from tinycrawler.utils import ip
from requests import RequestException
from .utils import default_ip, mock_ip_success, mock_ip_failures
from httmock import HTTMock


def test_ip():
    """Test to see if everything is working within ip."""
    with HTTMock(mock_ip_success):
        assert default_ip == ip()

    try:
        with HTTMock(mock_ip_failures):
            ip()
    except RequestException:
        pass
