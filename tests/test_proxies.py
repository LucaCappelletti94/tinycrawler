from tinycrawler.data import Proxies
from tinycrawler import Domain


def test_proxies():
    proxies = Proxies(path="test_data/raw_proxies.json")
    proxies.pop(Domain("https://www.youtube.com/watch?v=aVIXCdt7Ndg"))
