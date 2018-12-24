from ..sporadic_sequential_expirable import SporadicSequentialExpirable
from typing import Dict
import json


class Response(SporadicSequentialExpirable):
    def __init__(self, text: str, status: int, url: str, **kwargs):
        super(Response, self).__init__(**kwargs)
        self._text = text
        self._status = status
        self._url = url

    @property
    def text(self)->str:
        return self._text

    @property
    def json(self)->Dict:
        return json.loads(self._text)

    @property
    def status(self)->int:
        return self._status

    @property
    def url(self)->str:
        return self._url
