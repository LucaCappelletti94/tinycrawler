"""Test representation against expected one for given object."""


def format_repr_path(obj, char=""):
    if char:
        char = "_"+char
    return "test_data/expected_{obj}{char}_representation.json".format(obj=obj.__class__.__name__.lower(), char=char)


def mock_repr(obj, char=""):
    """Test representation against expected one for given object."""
    with open(format_repr_path(obj, char), "r") as f:
        assert str(obj) == f.read()


def build_repr(obj, char=""):
    """Prepares test representation for given object."""
    with open(format_repr_path(obj, char), "w") as f:
        f.write(str(obj))
