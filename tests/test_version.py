"""Test for version file syntax."""
import re

from tinycrawler.__version__ import __version__


def test_version():
    pattern = re.compile(r"\d+\.\d+\.\d+")
    assert pattern.match(__version__)
