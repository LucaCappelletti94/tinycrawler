from tinycrawler.expirables import Proxy
from ..utils.test_proxy_data import setup as setup_proxy_data
from ..commons import mock_repr
from .test_url import setup as setup_url


def setup(path=None)->Proxy:
    return Proxy(setup_proxy_data(path), maximum_usages=1)


def test_proxy():
    proxy = setup()
    proxy_b = setup("proxy_data_B")

    url = setup_url()
    proxy.use(
        domain=url.domain
    )
    try:
        proxy.use(
            domain=url.domain
        )
        assert False
    except AssertionError:
        pass

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
    mock_repr(setup())
