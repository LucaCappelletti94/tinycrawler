from tinycrawler.validators import path


def test_path():
    assert path("lo/kebabbo/bello.html")
    assert not path("lo/kebabbo/bello.html/")
    assert not path("lo/kebabbo/bello")
    assert not path("lo/kebabbo/bello???.html")
    assert not path("lo:kebabbo/bello.html")
    assert not path("lo//kebabbo/bello.html")
