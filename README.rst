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

TODOs for next version
------------------------

- Test proxies while normally downloading. - DONE
- Parallelize different domains downloads. - DONE
- Add dropping for high failure proxy and add parameters for such rate - DONE, yet to be tested
- Make failure rate domain specific with also a global mean.
- Enable failure rate also for local.
- Check robots txt also before downloading urls
- Reduce robots timeout defaults to 2 hours
- Change to exponential the wait timeout for the download attempts
- To define a binary file, check if in the first 1000 characters you find a number greater than 3/5 of zeros
- Add useragent
- Stop downloads when all proxies are dead.
- Try to use `active_children` as a way to test for active processes
- Add test for proxies
- Add way to save progress automatically every given timeout. 
- Add way to automatically save tested proxies.

Preview (Test case)
---------------------
This is the preview of the console when running the `test_base.py`_.

|preview|

Basic usage example
---------------------

.. code:: python

    from tinycrawler import TinyCrawler, Log
    from bs4 import BeautifulSoup


    def url_validator(url: str, logger: Log)->bool:
        """Return a boolean representing if the crawler should parse given url."""
        return url.startswith("http://interestingurl.com")


    def file_parser(url:str, soup:BeautifulSoup, logger: Log):
        """Parse and elaborate given soup."""
        # soup parsing...
        pass

    TinyCrawler(
        file_parser=file_parser,
        url_validator=url_validator
    ).run("https://www.example.com/")

Example loading proxies
---------------------

.. code:: python

    from tinycrawler import TinyCrawler, Log
    from bs4 import BeautifulSoup


    def url_validator(url: str, logger: Log)->bool:
        """Return a boolean representing if the crawler should parse given url."""
        return url.startswith("http://interestingurl.com")


    def file_parser(url:str, soup:BeautifulSoup, logger: Log):
        """Parse and elaborate given soup."""
        # soup parsing...
        pass

    crawler = TinyCrawler(
        file_parser=file_parser,
        url_validator=url_validator
    )
    crawler.load_proxies("http://myexampletestserver.com", "path/to/proxies.json")
    crawler.run("https://www.example.com/")



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
