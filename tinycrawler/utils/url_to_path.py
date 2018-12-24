from urllib.parse import urlparse
import re
pattern = re.compile(r"^.+\..+$")


def url_to_path(url: str)->str:
    global pattern
    parsed = urlparse(url.replace(" ", "_"))
    path = parsed.path
    return "{domain}/{path}{filename}".format(
        domain=parsed.netloc,
        path=path.strip("/"),
        filename="/index.html" if path.endswith(
            "/") or not path or not pattern.match(path.split("/")[-1]) else ""
    ).replace("//", "/")
