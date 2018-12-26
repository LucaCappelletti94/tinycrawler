from tinycrawler.expirables import ParserTask
from tinycrawler import IllegalArgumentError
from .test_response import setup as response_setup
from .test_response import default_url
from ..commons import mock_repr


def setup(response=None):
    task = ParserTask(response or response_setup())
    task.task_id = 0
    return task


def test_parser_task_arguments():
    response = response_setup()
    parser_task = setup(response)

    try:
        parser_task.urls
    except AssertionError:
        pass

    parser_task.urls = set([default_url])
    assert parser_task.urls == set([default_url])

    try:
        parser_task.urls = set([default_url])
    except AssertionError:
        pass

    assert parser_task.response == response

    parser_task.use()
    parser_task.used()

    try:
        parser_task.page
    except AssertionError:
        pass

    try:
        parser_task.path
    except AssertionError:
        pass

    invalid_paths = [
        "test/my_file/",
        "test/my_file//",
        "test/my_file//\"",
        "test/my_file?/"
    ]

    for path in invalid_paths:
        try:
            parser_task.path = path
            assert False
        except IllegalArgumentError:
            pass

    path = "test/my_file.txt"
    content = "my page content"

    parser_task.path = path
    parser_task.page = content

    try:
        parser_task.path = path
    except AssertionError:
        pass

    try:
        parser_task.page = content
    except AssertionError:
        pass

    assert parser_task.page == content
    assert parser_task.path == path


def test_parser_task_repr():
    mock_repr(setup())
