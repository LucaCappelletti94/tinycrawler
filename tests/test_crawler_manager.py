from tinycrawler.managers.crawler_manager import CrawlerManager
from .commons import mock_repr


def setup():
    return CrawlerManager("", 0, b"abc")


def test_crawler_manager():
    manager = setup()
    for endpoint in manager.endpoints:
        try:
            if endpoint == "register_client":
                getattr(manager, endpoint)(None)
            else:
                getattr(manager, endpoint)()
            print(
                "Endpoint {endpoint} did not raise NotImplementedError.".format(
                    endpoint=endpoint
                )
            )
            assert False
        except NotImplementedError:
            pass


def test_crawler_manager_test():
    mock_repr(setup())
