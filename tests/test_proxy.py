from tinycrawler.expirables import Proxy
from tinycrawler.utils import ProxyData
from tinycrawler import Domain, Url
import json


def test_proxy():
    with open("test_data/raw_proxy_data.json", "r") as f:
        proxy_data = ProxyData(json.load(f))

    domain = Domain("78.38.241.9")
    domainb = Domain("78.200.241.9")

    proxy = Proxy(domain, proxy_data)
    proxyb = Proxy(domainb, proxy_data)

    url = Url("https://www.youtube.com/watch?v=sUmoMSU9_GQ")
    proxy.use(url)
    proxy.used(url, success=False)

    assert proxy != proxyb
