from tinycrawler.expirables import Proxy
from tinycrawler.utils import ProxyData
from tinycrawler import Domain, Url, UnavailableError
import json


def test_proxy():
    with open("test_data/raw_proxy_data.json", "r") as f:
        proxy_data = ProxyData(json.load(f))

    domain = Domain("78.38.241.9")
    domainb = Domain("78.200.241.9")

    proxy = Proxy(domain, proxy_data, maximum_usages=1)
    proxyb = Proxy(domainb, proxy_data)

    url = Url("https://www.youtube.com/watch?v=sUmoMSU9_GQ")
    proxy.use(url)
    try:
        proxy.use(url)
        assert False
    except UnavailableError:
        pass

    proxy.used(url, success=False)
    proxy.use(url)

    proxy.local

    assert proxy != proxyb
    assert proxy.data == proxy_data

    with open("test_data/expected_proxy_representation.json", "r") as f:
        assert str(proxy) == f.read()
