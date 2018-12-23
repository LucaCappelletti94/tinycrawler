from tinycrawler.managers.crawler_manager import CrawlerManager


def test_crawler_manager():
    manager = CrawlerManager("", 0, b"abc")
    print(manager.endpoints)
