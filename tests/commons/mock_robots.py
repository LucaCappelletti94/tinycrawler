import httpretty
from .various import build_default_url

default_robots_url = build_default_url("/robots.txt")


def mock_robots(path: str = "test_data/robots.txt"):
    global default_robots_url
    with open(path, "r") as f:
        httpretty.register_uri(
            httpretty.GET,
            default_robots_url,
            body=f.read(),
            content_type="text/plain"
        )


def mock_sensitive_robots():
    mock_robots("test_data/robots_sensitive.txt")