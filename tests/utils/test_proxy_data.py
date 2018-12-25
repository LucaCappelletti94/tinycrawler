from tinycrawler.utils import ProxyData
from ..commons import mock_repr
import json


def setup()->ProxyData:
    with open("test_data/raw_proxy_data.json", "r") as f:
        return ProxyData(data=json.load(f))


def test_proxy_data():
    setup()


def test_proxy_data_repr():
    mock_repr(setup())
