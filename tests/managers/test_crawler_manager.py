from tinycrawler.managers.crawler_manager import CrawlerManager
from ..commons import mock_repr
import pytest


def crawler_manager_setup():
    return CrawlerManager("", 0, b"abc")


def test_crawler_manager():
    manager = crawler_manager_setup()
    for endpoint in manager.endpoints:
        with pytest.raises(NotImplementedError):
            if endpoint == "register_client":
                getattr(manager, endpoint)(None)
            else:
                getattr(manager, endpoint)()


def test_crawler_manager_test():
    mock_repr(crawler_manager_setup())
