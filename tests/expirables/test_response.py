from tinycrawler.expirables import Response
from ..commons import mock_repr

default_url = "http://docs.python-requests.org/en/master/api/#requests.Response.status_code"
default_status = 200
with open("test_data/successfull_download.html", "r") as f:
    default_content = f.read()


def response_setup(content=None, status=None, url=None)->Response:
    global default_url, default_status, default_content
    return Response(
        content or default_content,
        status or default_status,
        url or default_url
    )


def test_response():
    global default_url, default_status, default_content
    response = response_setup()
    assert response.url == default_url
    assert response.status == default_status
    assert response.text == default_content


def test_response_repr():
    mock_repr(response_setup())
