from tinycrawler import Domain
from ..commons import mock_repr


def setup():
    return Domain(
        "https://github.com/LucaCappelletti94/tinycrawler",
        maximum_consecutive_errors=1,
        maximum_error_rate=0.5
    )


def test_domain():
    assert setup() == setup()


def test_domain_repr():
    mock_repr(setup())
