"""Test if crawler is working."""
import hashlib
import json
import os
import random
import traceback

import pytest
import requests
from httmock import HTTMock, all_requests, response

import tinycrawler
from tinycrawler import TinyCrawler

path = os.path.dirname(__file__) + "/../test_data/base_test.html"
empty_proxy_path = os.path.dirname(__file__) + "/../test_data/empty_proxy.json"

WEBSITE_SIZE = 500
download_directory = "local_test"

root = "https://www.example.com"
anchor = "<a href='%s'>Link to page alias number %s</a>"


@all_requests
def example_mock(url, request):
    global path
    global root
    global anchor
    global WEBSITE_SIZE
    headers = {'content-type': 'text/html'}

    with open(path, "r") as f:
        model = f.read()

    links = ""
    rand = random.Random()
    rand.seed(int(url.path.split('/')[-1]))
    for i in range(10):
        j = rand.randint(0, WEBSITE_SIZE)
        link = "%s/%s" % (root, j)
        links += anchor % (link, j)

    body = model.replace("{PLACEHOLDER}", links)
    return response(200, body, headers, None, 5, request)


def check_files(path, root, anchor, download_directory, size):
    errors = []

    with open(path, "r") as f:
        model = f.read()

    rand = random.Random()

    for k in range(0, size - 1):
        links = ""
        url = "%s/%s" % (root, k)
        rand.seed(k)
        for i in range(10):
            j = rand.randint(0, size)
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
            errors.append("File %s does not match expected: %s != %s" % (
                file_name, json.dumps(output, indent=4), json.dumps(content, indent=4)))
            break

    return errors


def test_base_tinycrawler():
    global path
    global root
    global anchor
    global download_directory
    global empty_proxy_path
    global WEBSITE_SIZE

    with HTTMock(example_mock):
        my_crawler = TinyCrawler(use_cli=True, directory=download_directory)
        my_crawler.set_proxy_timeout(0)
        my_crawler.set_url_validator(tinycrawler.process.UrlParser._tautology)
        my_crawler.set_file_parser(tinycrawler.process.FileParser._parser)
        my_crawler.set_retry_policy(tinycrawler.process.Downloader._retry)
        my_crawler.load_proxies(root, empty_proxy_path)
        my_crawler.run(root + "/%s" % WEBSITE_SIZE)

    file_count = check_files(
        path, root, anchor, download_directory, WEBSITE_SIZE)

    assert not file_count, "errors occured:\n{}".format("\n".join(file_count))
