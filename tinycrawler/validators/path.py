"""Check if given path is valid, trying to avoid possible errors in every system."""


def path(path: str, special_chars: str = ":|<>?\"*%\\ \0")->bool:
    """Check if given path is valid, trying to avoid possible errors in every system.
        path:str, path to check for.
        special_chars: str, characters that are not allowed in the path.
    """
    assert isinstance(path, str)
    assert isinstance(special_chars, str)
    return path == path.lower() and all([s not in path for s in special_chars]) and "//" not in path and path[-1] != "/" and "." in path
