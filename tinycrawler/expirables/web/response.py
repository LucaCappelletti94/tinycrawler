"""Create a sporadically, sequentially available response object that can expire."""
from ..sporadic_sequential_expirable import SporadicSequentialExpirable
from typing import Dict


class Response(SporadicSequentialExpirable):
    """Create a sporadically, sequentially available response object that can expire."""

    def __init__(self, text: str, status: int, url: str, **kwargs):
        """Create a sporadically, sequentially available response object that can expire.
            text: str, textual response.
            status: int, response status of the request.
            url: str, url response from which the request was made.
        """
        super(Response, self).__init__(**kwargs)
        self._text = text
        self._status = status
        self._url = url

    @property
    def text(self)->str:
        """Return text object."""
        return self._text

    @property
    def status(self)->int:
        """Return response status."""
        return self._status

    @property
    def url(self)->str:
        """Return url to where the request was made."""
        return self._url

    def __eq__(self, other)->bool:
        return other is not None and isinstance(other, Response) and self.status == other.status and self.url == other.url and self.text == other.text

    def ___repr___(self)->Dict:
        """Return a dictionary representation of object."""
        return {
            **super(Response, self).___repr___(),
            **{
                "text": self.text,
                "status": self.status,
                "url": self.url,
            }}
