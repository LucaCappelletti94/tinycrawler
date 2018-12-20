from tinycrawler import Url
from .utils import double_arguments_test


def test_url_arguments():
    valid = {
        "url": ["https://sonarcloud.io/component_measures?branch=Tinycrawler2&id=tinycrawler.lucacappelletti&metric=new_coverage"]
    }
    invalid = {
        "url": ["Ciao mi chiamo gustavo, gustavo la pasta."]
    }

    double_arguments_test(Url, valid, invalid)


def test_url():
    url_1 = Url("https://www.youtube.com/watch?v=LxtppUZthug")
    url_2 = Url("https://www.youtube.com/watch?")

    assert url_1 != url_2

    assert url_1.timeout == 0

    with open("test_data/expected_url_representation.json", "r") as f:
        assert str(url_1) == f.read()
