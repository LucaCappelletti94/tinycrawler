"""Test representation against expected one for given object."""


def format_repr_path(obj):
    return "test_data/expected_{obj}_representation.json".format(obj=obj.__class__.__name__.lower())


def mock_repr(obj):
    """Test representation against expected one for given object."""
    with open(format_repr_path(obj), "r") as f:
        assert str(obj) == f.read()


def build_repr(obj):
    """Prepares test representation for given object."""
    with open(format_repr_path(obj), "w") as f:
        f.write(str(obj))
