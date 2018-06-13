.. role:: py(code)
   :language: python

.. role:: json(code)
   :language: json


Tinycrawler
====================

|travis| |coveralls| |sonar_quality| |sonar_maintainability| |code_climate_maintainability| |code_climate_test_coverage| |pip|

A small crawler that uses multiprocessing and arbitrarily many proxies to download one or more websites following a given filter, search and save functions.

**REMEMBER THAT DDOS IS ILLEGAL. DO NOT THIS SOFTWARE FOR ILLEGAL PORPOSES.**

Usage example
---------------------

.. code:: python

    #!/usr/bin/env python
    from urllib.parse import urlparse
    from tinycrawler import TinyCrawler
    from bs4 import BeautifulSoup


    def my_custom_validator(url):
        if "http://www.example.com/my/path" not in url:
            return False

        return True


    def my_file_parser(url, text, logger):
        return None
        soup = BeautifulSoup(text, 'lxml')

        example = soup.find("div", {"class": "example"})
        if example is None:
            return None

        return example.get_text()


    my_crawler = TinyCrawler(
        seed="http://www.example.com/my/path/index.html"
    )

    my_crawler.set_url_validator(my_custom_validator)
    my_crawler.set_file_parser(my_file_parser)

    my_crawler.run()


Proxies found on the web can be found in the file "proxies.json" and are in the following format:

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


.. |travis| image:: https://travis-ci.org/LucaCappelletti94/tinycrawler.png
   :target: https://travis-ci.org/LucaCappelletti94/tinycrawler

.. |coveralls| image:: https://coveralls.io/repos/github/LucaCappelletti94/distances/badge.svg?branch=master
    :target: https://coveralls.io/github/LucaCappelletti94/distances

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=tinycrawler.lucacappelletti&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/tinycrawler.lucacappelletti

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=tinycrawler.lucacappelletti&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/tinycrawler.lucacappelletti

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/25fb7c6119e188dbd12c/maintainability
   :target: https://codeclimate.com/github/LucaCappelletti94/tinycrawler/maintainability
   :alt: Maintainability

.. |code_climate_test_coverage| image:: https://api.codeclimate.com/v1/badges/25fb7c6119e188dbd12c/test_coverage
   :target: https://codeclimate.com/github/LucaCappelletti94/tinycrawler/test_coverage
   :alt: Test Coverage

.. |pip| image:: https://badge.fury.io/py/tinycrawler.svg
    :target: https://badge.fury.io/py/tinycrawler