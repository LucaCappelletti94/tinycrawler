from tinycrawler.utils import ProxyData
from ..commons import mock_repr
import json


def setup(path=None)->ProxyData:
    if path is None:
        path = "proxy_data"
    with open("test_data/raw_{path}.json".format(path=path), "r") as f:
        return ProxyData(data=json.load(f))


def test_proxy_data():
    setup()


def test_proxy_data_repr():
    mock_repr(setup())
