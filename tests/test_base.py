"""Test if crawler is working."""
import os
import re
import random
import shutil
from bs4 import BeautifulSoup
from filecmp import dircmp
import pytest
from httmock import HTTMock, all_requests, response

import tinycrawler
from tinycrawler import TinyCrawler, Log

model_path = os.path.dirname(__file__) + "/../test_data/base_test.html"

SIZE = 200
LINKS = 135
test_root = "test_root"
download_path, generation_path = "{test_root}/download".format(
    test_root=test_root), "{test_root}/generation".format(test_root=test_root)

root = "https://www.example.com"


def purge(pattern):
    for f in os.listdir():
        if re.search(pattern, f):
            shutil.rmtree(f)


def generate_links(link_number: int, rand: random.Random, root: str, size: int):
    anchor = '<a href="{root}/{page_number}">Link to page alias number {page_number}</a>'
    return "".join([
        anchor.format(root=root, page_number=rand.randint(0, size))
        for i in range(link_number)])


@all_requests
def example_mock(url, request):
    global model_path, SIZE, LINKS, generation_path, root

    seed = int(url.path.split('/')[-1])
    rand = random.Random()
    rand.seed(seed)

    with open(model_path, "r") as f_in, open("{generation_path}/{seed}.html".format(generation_path=generation_path, seed=seed), "w") as f_out:
        body = f_in.read().format(PLACEHOLDER=generate_links(
            LINKS, rand, root, SIZE))
        f_out.write(str(BeautifulSoup(body, "html5lib")))

    return response(content=body, headers={'content-type': 'text/html'}, request=request)


def file_parser(url: str, soup: BeautifulSoup, log: Log):
    global download_path
    with open("{download_path}/{seed}.html".format(download_path=download_path, seed=url.split('/')[-1]), "w") as f_out:
        f_out.write(str(soup))


def url_validator(url: str, log: Log):
    return True


def test_base_tinycrawler():
    global root, SIZE, download_path, generation_path, test_root

    os.makedirs(download_path, exist_ok=True)
    os.makedirs(generation_path, exist_ok=True)
    seed = "{root}/{website_size}".format(root=root, website_size=SIZE)
    with HTTMock(example_mock):
        TinyCrawler(file_parser, url_validator, proxy_timeout=0).run(seed)

    downloaded_files_number = len([f for _, _, files in os.walk(
        download_path) for f in files if f.endswith(".html")])
    differences = dircmp(download_path, generation_path).diff_files
    purge(test_root)

    assert not differences and downloaded_files_number == SIZE+1
