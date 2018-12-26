from tinycrawler.expirables import Response
import json
from ..commons import mock_repr

default_url = "http://docs.python-requests.org/en/master/api/#requests.Response.status_code"
default_status = 200
default_content = ["I", "am", "content"]


def setup(content=None, status=None, url=None)->Response:
    global default_url, default_status, default_content
    return Response(
        json.dumps(content or default_content),
        status or default_status,
        url or default_url
    )


def test_response():
    global default_url, default_status, default_content
    response = setup()
    assert response.url == default_url
    assert response.status == default_status
    assert response.json == default_content


def test_response_repr():
    mock_repr(setup())
