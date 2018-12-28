from tinycrawler.expirables import ParserTask
from tinycrawler import IllegalArgumentError
from .test_response import setup as response_setup
from .test_response import default_url
from ..commons import mock_repr
import pytest


def setup(response=None):
    task = ParserTask(response or response_setup())
    task.task_id = 0
    return task


def test_parser_task_arguments():
    response = response_setup()
    parser_task = setup(response)

    with pytest.raises(AssertionError):
        parser_task.urls

    parser_task.urls = set([default_url])
    assert parser_task.urls == set([default_url])

    with pytest.raises(AssertionError):
        parser_task.urls = set([default_url])

    assert parser_task.response == response

    parser_task.use()
    parser_task.used()

    with pytest.raises(AssertionError):
        parser_task.page

    with pytest.raises(AssertionError):
        parser_task.path

    invalid_paths = [
        "test/my_file/",
        "test/my_file//",
        "test/my_file//\"",
        "test/my_file?/"
    ]

    for path in invalid_paths:
        with pytest.raises(IllegalArgumentError):
            parser_task.path = path

    path = "test/my_file.txt"
    content = "my page content"

    parser_task.path = path
    parser_task.page = content

    with pytest.raises(AssertionError):
        parser_task.path = path

    with pytest.raises(AssertionError):
        parser_task.page = content

    assert parser_task.page == content
    assert parser_task.path == path


def test_parser_task_repr():
    mock_repr(setup())
