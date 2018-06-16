"""Test if crawler is working."""
import hashlib
import json
import os
import random
import traceback
from multiprocessing import Lock

import pytest
import requests
from httmock import HTTMock, all_requests, response

import tinycrawler
from tinycrawler import TinyCrawler

path = os.path.dirname(__file__) + "/../test_data/base_test.html"

download_directory = "local_test"

root = "https://www.example.com"
anchor = "<a href='%s'>Link to page alias number %s</a>"


@all_requests
def example_mock(url, request):
    global path
    global root
    global anchor
    global lock
    headers = {'content-type': 'text/html'}

    with open(path, "r") as f:
        model = f.read()

    links = ""
    random.seed(int(url.path.split('/')[-1]))
    for i in range(10):
        j = random.randint(0, 999)
        link = "%s/%s" % (root, j)
        links += anchor % (link, j)

    body = model.replace("{PLACEHOLDER}", links)
    return response(200, body, headers, None, 5, request)


def check_files(path, root, anchor, download_directory):
    errors = []

    with open(path, "r") as f:
        model = f.read()

    for k in range(0, 1000):
        links = ""
        random.seed(k)
        url = "%s/%s" % (root, k)
        for i in range(10):
            j = random.randint(0, 999)
            link = "%s/%s" % (root, j)
            links += anchor % (link, j)
        body = model.replace("{PLACEHOLDER}", links)
        h = hashlib.md5(url.encode('utf-8')).hexdigest()
        file_name = "%s/website/1/%s.json" % (download_directory, h)

        content = {
            "url": url,
            "content": body
        }

        if not os.path.exists(file_name):
            errors.append("File %s does not exist." % file_name)
            break

        with open(file_name, "r") as f:
            output = json.load(f)

        if output != content:
            errors.append("File %s does not match expected" % (file_name))
            break

    return errors


def test_base_tinycrawler():
    global path
    global root
    global anchor
    global download_directory

    with HTTMock(example_mock):
        my_crawler = TinyCrawler(use_cli=True, directory=download_directory)
        my_crawler.set_proxy_timeout(0)
        my_crawler.set_url_validator(tinycrawler.process.UrlParser._tautology)
        my_crawler.set_file_parser(tinycrawler.process.FileParser._parser)
        my_crawler.set_retry_policy(tinycrawler.process.Downloader._retry)
        my_crawler.run(root + "/1000")

    file_count = check_files(path, root, anchor, download_directory)

    assert not file_count, "errors occured:\n{}".format("\n".join(file_count))
