from tinycrawler.utils import ProxyData
from ..commons import mock_repr
from ..expirables.test_client_data import setup as client_data_setup
import json


def setup(path=None)->ProxyData:
    if path is None:
        path = "proxy_data"
    with open("test_data/raw_{path}.json".format(path=path), "r") as f:
        return ProxyData(data=json.load(f))


def setup_local()->ProxyData:
    return ProxyData(ip=client_data_setup().ip)


def test_proxy_data():
    setup()
    setup_local()


def test_proxy_data_repr():
    mock_repr(setup())
