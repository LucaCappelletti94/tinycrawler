"""Test if crawler is working."""
import os
import random
import traceback

import pytest
import requests
from httmock import HTTMock, all_requests, response

from tinycrawler import TinyCrawler

random.seed(42)  # For reproducibility

path = os.path.dirname(__file__) + "/../test_data/base_test.html"
root = "https://www.example.com"
anchor = "<a href='%s'>Link to page alias number %s</a>"


@all_requests
def example_mock(url, request):
    global path
    global root
    global anchor
    headers = {'content-type': 'text/html'}
    links = ""

    with open(path, "r") as f:
        model = f.read()

    for i in range(10):
        j = random.randint(0, 999)
        url = "%s/%s" % (root, j)
        links += anchor % (url, i)

    body = model.replace("{PLACEHOLDER}", links)
    return response(200, body, headers, None, 5, request)


def test_base_tinycrawler():
    global root

    with HTTMock(example_mock):
        my_crawler = TinyCrawler(use_cli=True)
        my_crawler.set_proxy_timeout(0)
        my_crawler.run(root)

    """If it gets here without crashing I'm happy for now"""
    assert True
