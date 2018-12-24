from tinycrawler.expirables import ParserTask, Response
from tinycrawler import IllegalArgumentError, Url
from .utils import double_arguments_test


def test_parser_task_arguments():
    try:
        ParserTask(None, 0)
        assert False
    except IllegalArgumentError:
        pass

    url = "https://requests-mock.readthedocs.io/en/latest/response.html"

    parser_task = ParserTask(Response("", 200, url), 0)

    parser_task.add_url(
        Url(url))
    parser_task.urls

    parser_task.use()
    parser_task.used()

    try:
        parser_task.page
    except ValueError:
        pass

    try:
        parser_task.path
    except ValueError:
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

    parser_task.path = "test/my_file.txt"
    parser_task.page = "my page content"

    try:
        parser_task.path = "Trying to set again path"
        assert False
    except ValueError:
        pass

    try:
        parser_task.page = "Trying to set again page"
        assert False
    except ValueError:
        pass

    parser_task.page
    parser_task.path

    with open("test_data/expected_parser_task_representation.json", "r") as f:
        assert str(parser_task) == f.read()
