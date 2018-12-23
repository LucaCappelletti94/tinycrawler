from tinycrawler.managers.crawler_manager import CrawlerManager


def test_crawler_manager():

    manager = CrawlerManager("", 0, b"abc")

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
