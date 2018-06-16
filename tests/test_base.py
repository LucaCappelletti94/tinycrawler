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

download_directory = "local_test"

root = "https://www.example.com"
anchor = "<a href='%s'>Link to page alias number %s</a>"


@all_requests
def example_mock(url, request):
    global path
    global root
    global anchor
    headers = {'content-type': 'text/html'}

    with open(path, "r") as f:
        model = f.read()

    links = ""
    for i in range(10):
        j = random.randint(0, 999)
        url = "%s/%s" % (root, j)
        links += anchor % (url, i)

    body = model.replace("{PLACEHOLDER}", links)
    return response(200, body, headers, None, 5, request)


def check_files():
    global path
    global root
    global anchor
    global download_directory
    random.seed(42)

    with open(path, "r") as f:
        model = f.read()

    for i in range(0, 1000):
        links = ""
        for i in range(10):
            j = random.randint(0, 999)
            url = "%s/%s" % (root, j)
            links += anchor % (url, i)
        body = model.replace("{PLACEHOLDER}", links)
        file_name = "%s/website/1/%s" % (download_directory, hash(url))

        if not os.path.exists(file_name):
            return False

        with open(file_name, "r") as f:
            output = f.read()

        if output != body:
            return False

    return True


def test_base_tinycrawler():
    global root
    global download_directory
    with HTTMock(example_mock):
        my_crawler = TinyCrawler(use_cli=True, directory=download_directory)
        my_crawler.set_proxy_timeout(0)
        my_crawler.run(root)

    file_count = check_files()

    return file_count
