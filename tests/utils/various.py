default_url = "http://www.totallyfakeexample.com"


def build_default_url(path: str = ""):
    global default_url
    return "{default}{path}".format(
        default=default_url,
        path=path
    )
