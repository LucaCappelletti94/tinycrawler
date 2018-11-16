.. role:: py(code)
   :language: python

.. role:: json(code)
   :language: json


TinyCrawler
====================

|travis| |sonar_quality| |sonar_maintainability| |sonar_coverage| |code_climate_maintainability| |pip|

An highly customizable crawler that uses multiprocessing and proxies to download one or more websites following a given filter, search and save functions.

**REMEMBER THAT DDOS IS ILLEGAL. DO NOT USE THIS SOFTWARE FOR ILLEGAL PURPOSE.**

Installing TinyCrawler
------------------------

.. code:: shell

    pip install tinycrawler


Preview (Test case)
---------------------
This is the preview of the console when running the `test_base.py`_.

|preview|

Usage example
---------------------

.. code:: python

    from tinycrawler import TinyCrawler, Log, Statistics
    from bs4 import BeautifulSoup, SoupStrainer
    import pandas as pd
    from requests import Response
    from urllib.parse import urlparse
    import os
    import json


    def html_sanitization(html: str) -> str:
        """Return sanitized html."""
        return html.replace("WRONG CONTENT", "RIGHT CONTENT")


    def get_product_name(response: Response) -> str:
        """Return product name from given Response object."""
        return response.url.split("/")[-1].split(".html")[0]


    def get_product_category(soup: BeautifulSoup) -> str:
        """Return product category from given BeautifulSoup object."""
        return soup.find_all("span")[-2].get_text()


    def parse_tables(html: str, path: str, strainer: SoupStrainer):
        """Parse table at given strained html object saving them as csv at given path."""
        for table in BeautifulSoup(
                html, "lxml", parse_only=strainer).find_all("table"):
            df = pd.read_html(html_sanitization(str(table)))[0].drop(0)
            table_name = df.columns[0]
            df.set_index(table_name, inplace=True)
            df.to_csv("{path}/{table_name}.csv".format(
                path=path, table_name=table_name))


    def parse_metadata(html: str, path: str, strainer: SoupStrainer):
        """Parse metadata from given strained html and saves them as json at given path."""
        with open("{path}/metadata.json".format(path=path), "w") as f:
            json.dump({
                "category":
                get_product_category(
                    BeautifulSoup(html, "lxml", parse_only=strainer))
            }, f)


    def parse(response: Response):
        path = "{root}/{product}".format(
            root=urlparse(response.url).netloc, product=get_product_name(response))
        if not os.path.exists(path):
            os.makedirs(path)
        parse_tables(
            response.text, path,
            SoupStrainer(
                "table",
                attrs={"class": "table table-hover table-condensed table-fixed"}))

        parse_metadata(
            response.text, path,
            SoupStrainer("span"))


    def url_validator(url: str, logger: Log, statistics: Statistics)->bool:
        """Return a boolean representing if the crawler should parse given url."""
        return url.startswith("https://www.example.com/it/alimenti"")


    def file_parser(response: Response, logger: Log, statistics):
        if response.url.endswith(".html"):
            parse(response)


    seed = "https://www.example.com/it/alimenti"
    crawler = TinyCrawler(follow_robots_txt=False)
    crawler.set_file_parser(file_parser)
    crawler.set_url_validator(url_validator)

    crawler.load_proxies("http://mytestserver.domain", "proxies.json")

    crawler.run(seed)



Proxies are expected to be in the following format:

.. code:: python

    [
      {
        "ip": "89.236.17.108",
        "port": 3128,
        "type": [
          "https",
          "http"
        ]
      },
      {
        "ip": "128.199.141.151",
        "port": 3128,
        "type": [
          "https",
          "http"
        ]
      }
    ]


License
--------------
The software is released under the MIT license.

.. _`test_base.py`: https://github.com/LucaCappelletti94/tinycrawler/blob/master/tests/test_base.py

.. |preview| image:: https://github.com/LucaCappelletti94/tinycrawler/blob/master/preview.png?raw=true

.. |travis| image:: https://travis-ci.org/LucaCappelletti94/tinycrawler.png
   :target: https://travis-ci.org/LucaCappelletti94/tinycrawler

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=tinycrawler.lucacappelletti&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/tinycrawler.lucacappelletti

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=tinycrawler.lucacappelletti&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/tinycrawler.lucacappelletti

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=tinycrawler.lucacappelletti&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/tinycrawler.lucacappelletti

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/25fb7c6119e188dbd12c/maintainability
   :target: https://codeclimate.com/github/LucaCappelletti94/tinycrawler/maintainability
   :alt: Maintainability

.. |pip| image:: https://badge.fury.io/py/tinycrawler.svg
    :target: https://badge.fury.io/py/tinycrawler
