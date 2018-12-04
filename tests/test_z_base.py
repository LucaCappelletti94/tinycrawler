"""Test if crawler is working."""
import os
import re
import random
import shutil
from bs4 import BeautifulSoup
from filecmp import dircmp
from httmock import HTTMock, all_requests, response
from httpretty import HTTPretty, httprettified
import requests

import tinycrawler
from tinycrawler import TinyCrawler, Log

model_path = os.path.dirname(__file__) + "/../test_data/base_test.html"
robots_path = os.path.dirname(__file__) + "/../test_data/robots.txt"
proxy_path = os.path.dirname(__file__) + "/../test_data/proxies.json"

SIZE = 20
LINKS = 100
WEBSITES = 10
test_root = "test_root"
download_path, generation_path = "{test_root}/download".format(
    test_root=test_root), "{test_root}/generation".format(test_root=test_root)

with open(robots_path, "r") as f:
    robots_body = f.read()

with open(model_path, "r") as f:
    model_body = f.read()

root = "https://www.example{n}.com"


def purge(pattern):
    for f in os.listdir():
        if re.search(pattern, f):
            shutil.rmtree(f)


def generate_links(link_number: int, rand: random.Random, root: str, size: int, websites: int):
    anchor = '<a href="{root}/{page_number}">Link to page alias number {page_number}</a>'
    return "".join([
        anchor.format(root=root.format(n=rand.randint(1, websites)),
                      page_number=rand.randint(1, size))
        for i in range(link_number)])


@all_requests
def example_mock(url, request):
    global model_body, SIZE, LINKS, WEBSITES, generation_path, root

    seed = int(url.path.strip('/'))
    rand = random.Random()
    rand.seed(seed)

    if seed == 1:
        return response(status_code=404)
    if seed == 2:
        return response(content="", headers={'content-type': 'application/pdf'})
    if seed == 3:
        raise requests.ConnectionError

    path = "".join(url).replace("/", "_")
    with open("{generation_path}/{path}.html".format(generation_path=generation_path, path=path), "w") as f_out:
        body = model_body.format(PLACEHOLDER=generate_links(
            LINKS, rand, root, SIZE, WEBSITES))
        f_out.write(str(BeautifulSoup(body, "html5lib")))

    return response(content=body, headers={'content-type': 'text/html'}, request=request)


def file_parser(url: str, soup: BeautifulSoup, log: Log):
    global download_path
    path = url.replace("/", "_")
    with open("{download_path}/{path}.html".format(download_path=download_path, path=path), "w") as f_out:
        f_out.write(str(soup))


def url_validator(url: str, log: Log):
    return True


backup_robots = tinycrawler.robots.Robots._retrieve_robots_txt


@httprettified
def wrapped_robots(self, domain: str):
    global robots_body, WEBSITES
    for i in range(1, WEBSITES+1):
        HTTPretty.register_uri(HTTPretty.GET, "https://www.example{i}.com/robots.txt".format(i=i),
                               body=robots_body,
                               content_type="text/plain")
    backup_robots(self, domain)


tinycrawler.robots.Robots._retrieve_robots_txt = wrapped_robots


def test_base_tinycrawler():
    global root, SIZE, WEBSITES, download_path, generation_path, test_root, proxy_path
    os.makedirs(download_path, exist_ok=True)
    os.makedirs(generation_path, exist_ok=True)
    seed = "{root}/{website_size}".format(
        root=root.format(n=1), website_size=SIZE)
    with HTTMock(example_mock):
        TinyCrawler(file_parser=file_parser,
                    url_validator=url_validator, use_cli=True, proxy_timeout=0, domains_timeout=0, proxy_path=proxy_path, cooldown_time_beetween_download_attempts=0).run(seed)

    downloaded_files_number = len([f for _, _, files in os.walk(
        download_path) for f in files if f.endswith(".html")])
    differences = dircmp(download_path, generation_path).diff_files
    purge(test_root)

    assert not differences and downloaded_files_number == (SIZE-3)*WEBSITES
