# from .task import Task
# from ..web import Url
# from ...exceptions import IllegalArgumentError
# from typing import Set
# from requests import Response
# from ...validators import path as is_valid_path


# class DownloaderTask(Task):
#     def __init__(self, proxy: Proxy, task_id: int, **kwargs):
#         """Create an unique task.
#             task_id:int, unique identifier of current task.
#             response:Response, response to be parsed.
#         """
#         super(DownloaderTask, self).__init__(task_id, **kwargs)
#         if response is None:
#             raise IllegalArgumentError("Given response argument is None.")
#         self._response = response
#         self._urls = set()
#         self._page = self._path = None

#     @property
#     def response(self)->Response:
#         return self._response

#     @property
#     def page(self)->str:
#         if self._page is None:
#             raise ValueError("Page was not elaborated yet.")
#         return self._page

#     @property
#     def path(self)->str:
#         if self._path is None:
#             raise ValueError("Path was not elaborated yet.")
#         return self._path

#     @property
#     def urls(self)->Set[Url]:
#         return self._urls

#     @page.setter
#     def page(self, page: str):
#         if self._page is not None:
#             raise ValueError("Page has already been elaborated.")
#         self._page = page

#     @path.setter
#     def path(self, path: str):
#         if self._path is not None:
#             raise ValueError("Path has already been elaborated.")
#         if not is_valid_path(path):
#             raise IllegalArgumentError("Given path is not safe.")
#         self._path = path

#     def add_url(self, url: Url):
#         """Add given url to set."""
#         self._urls.add(url)

#     def ___repr___(self):
#         return {
#             **super(DownloaderTask, self).___repr___(),
#             **{
#                 "task_type": "downloader task"
#             }}
