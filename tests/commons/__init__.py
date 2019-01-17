from .utils import double_arguments_test
from .mock_ip import mock_ip_failures, mock_ip_success, default_ip
from .mock_robots import default_robots_url, mock_robots, mock_sensitive_robots
from .various import default_url, build_default_url
from .repr import mock_repr, build_repr
from .sleep import sleep
import platform


def mock_platform(*args)->str:
    """Method to mock calls to platform."""
    return "Mocked platform"


platform.platform = mock_platform

__all__ = [
    "double_arguments_test",
    "mock_ip_failures",
    "mock_ip_success",
    "default_ip",
    "default_url",
    "build_default_url",
    "default_robots_url",
    "mock_robots",
    "mock_sensitive_robots",
    "mock_repr",
    "build_repr",
    "sleep"
]
