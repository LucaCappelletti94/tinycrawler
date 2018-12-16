from tinycrawler import Domain
from .utils import double_arguments_test


def test_domain_arguments():
    valid = {
        "url": ["https://sonarcloud.io/component_measures?branch=Tinycrawler2&id=tinycrawler.lucacappelletti&metric=new_coverage"]
    }
    invalid = {
        "url": ["Ciao mi chiamo gustavo, gustavo la pasta."]
    }

    double_arguments_test(Domain, valid, invalid)


def test_domain():
    domain_1 = Domain("https://www.youtube.com/watch?v=LxtppUZthug")
    domain_2 = Domain("https://www.youtube.com/watch?")
    domain_3 = Domain(
        "https://coveralls.io/github/LucaCappelletti94/tinycrawler")
    assert domain_1 == domain_2
    assert domain_1 != domain_3

    with open("test_data/expected_domain_representation.json", "r") as f:
        assert str(domain_1) == f.read()
