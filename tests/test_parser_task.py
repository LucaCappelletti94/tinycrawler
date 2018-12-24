from tinycrawler.expirables import ParserTask, Response
from tinycrawler import IllegalArgumentError, Url


def test_parser_task_arguments():
    try:
        ParserTask(None, 0)
        assert False
    except IllegalArgumentError:
        pass

    url = "https://requests-mock.readthedocs.io/en/latest/response.html"

    response = Response("", 200, url)
    parser_task = ParserTask(response, 0)

    url_object = Url(url)

    try:
        parser_task.urls
        assert False
    except ValueError:
        pass

    parser_task.urls = set([url_object])
    assert parser_task.urls == set([url_object])

    try:
        parser_task.urls = set([url_object])
        assert False
    except ValueError:
        pass

    assert parser_task.response == response

    parser_task.use()
    parser_task.used()

    try:
        parser_task.page
        assert False
    except ValueError:
        pass

    try:
        parser_task.path
        assert False
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

    path = "test/my_file.txt"
    content = "my page content"

    parser_task.path = path
    parser_task.page = content

    try:
        parser_task.path = path
        assert False
    except ValueError:
        pass

    try:
        parser_task.page = content
        assert False
    except ValueError:
        pass

    assert parser_task.page == content
    assert parser_task.path == path

    with open("test_data/expected_parser_task_representation.json", "r") as f:
        assert str(parser_task) == f.read()
