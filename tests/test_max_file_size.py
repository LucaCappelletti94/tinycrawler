from tinycrawler.exceptions import MaxFileSize


def test_max_file_size():
    try:
        raise MaxFileSize()
        assert False
    except MaxFileSize:
        pass
