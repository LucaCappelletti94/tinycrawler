from urllib.parse import urlparse


def get_domain(url: str)->str:
    """Return domain from given url.
        url:str, the url from which extract the domain.
    """
    return '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(url))
