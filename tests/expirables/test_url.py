from tinycrawler import Url
from ..commons import double_arguments_test, mock_repr


def test_url_arguments():
    valid = {
        "url": ["https://sonarcloud.io/component_measures?branch=Tinycrawler2&id=tinycrawler.lucacappelletti&metric=new_coverage"]
    }
    invalid = {
        "url": ["Ciao mi chiamo gustavo, gustavo la pasta."]
    }

    double_arguments_test(Url, valid, invalid)


def url_setup(default: str = "https://www.totallyfakewebsite.com"):
    return Url(default)


def test_url():
    url_1 = url_setup()
    url_2 = url_setup("https://www.youtube.com/watch?")

    assert url_1 != url_2
    assert url_1.timeout == 0
    url_1.timeout = 0
    url_1.timeout = 3
    url_1.use()
    url_1.timeout = 4


def test_url_repr():
    mock_repr(url_setup())
