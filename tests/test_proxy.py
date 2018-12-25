from tinycrawler.expirables import Proxy
from tinycrawler.utils import ProxyData
from tinycrawler import Domain, Url, UnavailableError
import json


def test_proxy():
    with open("test_data/raw_proxy_data.json", "r") as f:
        proxy_data_A = ProxyData(data=json.load(f))
    with open("test_data/raw_proxy_data_B.json", "r") as f:
        proxy_data_B = ProxyData(data=json.load(f))

    proxy = Proxy(proxy_data_A, maximum_usages=1)
    proxyb = Proxy(proxy_data_B)

    url = Url("https://www.youtube.com/watch?v=sUmoMSU9_GQ")
    proxy.use(url.domain)
    try:
        proxy.use(url.domain)
        assert False
    except AssertionError:
        pass

    proxy.used(url.domain, success=False)
    proxy.use(url.domain)

    proxy.local

    assert proxy != proxyb
    assert proxy.data == proxy_data_A.data

    with open("test_data/expected_proxy_representation.json", "r") as f:
        assert str(proxy) == f.read()
