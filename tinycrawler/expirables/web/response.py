from ..sporadic_sequential_expirable import SporadicSequentialExpirable
from requests import Response as RequestsResponse


class Response(SporadicSequentialExpirable):
    def __init__(self, response: RequestsResponse, **kwargs):
        super(Response, self).__init__(**kwargs)
        self._response = response

    @property
    def response(self)->RequestsResponse:
        return self._response
