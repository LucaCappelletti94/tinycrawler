from tinycrawler.utils import ProxyData
import json
from pprint import pprint


def test_proxy_data():
    with open("test_data/raw_proxy_data.json", "r") as f, open("test_data/expected_proxy_data.json", "r") as expected:
        assert ProxyData(json.load(f)) == json.load(expected)
