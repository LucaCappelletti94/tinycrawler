from tinycrawler.expirables import Response
import json


def test_response():
    content = ["I", "am", "content"]
    textual_content = json.dumps(content)
    status = 200
    url = "http://docs.python-requests.org/en/master/api/#requests.Response.status_code"

    response = Response(textual_content, status, url)

    assert response.url == url
    assert response.status == status
    assert response.text == textual_content
    assert response.json == content
