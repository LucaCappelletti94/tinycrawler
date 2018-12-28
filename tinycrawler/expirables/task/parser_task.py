"""Create an unique parser task."""
from .task import Task
from ..web import Response
from ...exceptions import IllegalArgumentError
from typing import Set, Dict
from ...validators import path as is_valid_path


class ParserTask(Task):
    """Create an unique parser task."""

    def __init__(self, response: Response, **kwargs):
        """Create an unique parser task.
            response:Response, response to be parsed.
        """
        assert isinstance(response, Response)
        super(ParserTask, self).__init__(**kwargs)
        self._response = response
        self._urls = None
        self._page = self._path = None

    def use(self, **kwargs):
        """Update use status in response."""
        super(ParserTask, self).use(**kwargs)
        self._response.use(**kwargs)

    def used(self, **kwargs):
        """Update used status in response."""
        super(ParserTask, self).used()
        self._response.used(success=False)

    @property
    def response(self)->Response:
        """Return response object."""
        return self._response

    @property
    def page(self)->str:
        """Return parsed page string."""
        assert self._page is not None
        return self._page

    @property
    def path(self)->str:
        """Return path string."""
        assert self._path is not None
        return self._path

    @property
    def urls(self)->Set[str]:
        """Return urls."""
        assert self._urls is not None
        return self._urls

    @page.setter
    def page(self, page: str):
        """Set parsed page value.
            page:str, parsed page.
        """
        assert isinstance(page, str)
        assert self._page is None
        self._page = page

    @path.setter
    def path(self, path: str):
        """Set parsed path value.
            path:str, parsed path.
        """
        assert isinstance(path, str)
        assert self._path is None
        if not is_valid_path(path):
            raise IllegalArgumentError("Given path is not safe.")
        self._path = path

    @urls.setter
    def urls(self, urls: Set[str])->Set[str]:
        """Set extract urls set.
            urls:Set[str], extract urls set.
        """
        assert self._urls is None
        assert isinstance(urls, set)
        assert all([isinstance(url, str) for url in urls])
        self._urls = urls

    def ___repr___(self)->Dict:
        """Return a dictionary representation of object."""
        return {
            **super(ParserTask, self).___repr___(),
            **{
                "task_type": "parser task",
                "urls": sorted(list(self.urls)) if self._urls else None,
                "path": self.path if self._path else None,
                "page": self.page if self._page else None
            }}
