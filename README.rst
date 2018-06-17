.. role:: py(code)
   :language: python

.. role:: json(code)
   :language: json


Tinycrawler
====================

|travis| |sonar_quality| |sonar_maintainability| |sonar_coverage| |code_climate_maintainability| |pip|

A small crawler that uses multiprocessing and arbitrarily many proxies to download one or more websites following a given filter, search and save functions.

**REMEMBER THAT DDOS IS ILLEGAL. DO NOT THIS SOFTWARE FOR ILLEGAL PORPOSES.**

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

    from tinycrawler import TinyCrawler
    from bs4 import BeautifulSoup


    def url_validator(url:str)->bool:
        """Return if page at given url is to be downloaded."""
        if "http://www.example.com/my/path" not in url:
            return False

        return True

    def file_parser(self, request_url: str, text: str, logger: 'Log')->str:
        """Parse downloaded page into document to be saved.
            request_url: str, the url of given downloaded page
            text: str, the content of the page
            logger: 'Log', a logger to log eventual errors or infos

            Return None if the page should not be saved.
        """

        soup = BeautifulSoup(text, 'lxml')

        example = soup.find("div", {"class": "example"})
        if example is None:
            return None

        return example.get_text()


    my_crawler = TinyCrawler(use_cli=True, directory="my_path_for_website")

    my_crawler.load_proxies("path/to/my/proxies.json")
    my_crawler.set_url_validator(url_validator)
    my_crawler.set_file_parser(file_parser)

    my_crawler.run("http://www.example.com/my/path/index.html")


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

.. |preview| image:: https://github.com/LucaCappelletti94/tinycrawler/blob/master/preview.jpg?raw=true

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
