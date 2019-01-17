from tinycrawler.expirables import Proxy
from ..commons import mock_repr
from .test_url import url_setup
from ..utils.test_proxy_data import proxy_data_setup
import pytest


def proxy_setup(path=None)->Proxy:
    return Proxy(proxy_data_setup(path), maximum_usages=1)


def setup_local(path=None)->Proxy:
    return Proxy(proxy_data_setup(path), maximum_usages=1)


def test_proxy():
    proxy = proxy_setup()
    proxy_b = proxy_setup("proxy_data_B")

    url = url_setup()
    proxy.use(
        domain=url.domain
    )
    with pytest.raises(AssertionError):
        proxy.use(
            domain=url.domain
        )

    proxy.used(
        domain=url.domain,
        success=False
    )
    proxy.use(
        domain=url.domain
    )

    assert not proxy.local
    assert proxy != proxy_b


def test_proxy_repr():
    mock_repr(proxy_setup())
