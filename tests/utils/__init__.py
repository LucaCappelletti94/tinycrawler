from .utils import double_arguments_test
from .mock_ip import mock_ip_failures, mock_ip_success, default_ip
import platform


def mock_platform(*args)->str:
    """Method to mock calls to platform."""
    return "Mocked platform"


platform.platform = mock_platform

__all__ = [
    "double_arguments_test",
    "mock_ip_failures",
    "mock_ip_success",
    "default_ip"
]
