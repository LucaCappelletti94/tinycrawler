# Tinycrawler

A small crawler that uses multiprocessing and arbitrarily many proxies (for example a bot farm) to download one or more websites **THAT YOU HAVE RIGHTS TO DOWNLOAD** following a given filter function in the smaller possible amount of time.

**REMEMBER THAT DDOS IS ILLEGAL. DO NOT THIS SOFTWARE FOR ILLEGAL PORPOSES.**

## Usage example

```python
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
```

Proxies found on the web can be found in the file "proxies.json" and are in the following format:

```json
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
```

## License

MIT License

Copyright (c) 2018 Luca Cappelletti

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
