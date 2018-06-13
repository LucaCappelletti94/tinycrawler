"""Test if crawler is working."""
import os

import pytest
import requests
from httmock import HTTMock, all_requests, response

from tinycrawler import TinyCrawler


def no_file_parser(url, text, logger):
    """Return None to block file saving."""
    return text


body = ""


@all_requests
def example_mock(url, request):
    global body
    headers = {'content-type': 'text/html'}
    return response(200, body, headers, None, 5, request)


def test_base_tinycrawler():
    global body
    path = os.path.dirname(__file__) + "/../test_data/base_test.html"

    with open(path, "r") as f:
        data = f.read()

    url_pattern = "https://www.example.com/%s"
    anchor_pattern = "<a href='%s'>Link to page alias number %s</a>"

    links = ""
    n = 10

    for i in range(n):
        links += anchor_pattern % (url_pattern % i, i)

    body = data.replace("{PLACEHOLDER}", links)

    root = url_pattern % 0
    with HTTMock(example_mock):
        my_crawler = TinyCrawler(
            seed=root
        )

        my_crawler.set_file_parser(no_file_parser)

        my_crawler.run()

    """If it gets here without crashing I'm happy for now"""
    assert True
