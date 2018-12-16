def path(path: str, special_chars: str=":|<>?\"*%\\ \0"):
    """Check if given path is valid, trying to avoid possible errors in every system."""
    return path == path.lower() and all([s not in path for s in special_chars]) and "//" not in path and path[-1] != "/" and "." in path
