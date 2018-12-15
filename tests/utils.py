from tinycrawler.exceptions import IllegalArgumentError


def arguments_test(classname, valid, invalid):
    for key, values in valid.items():
        for value in values:
            try:
                classname(**{key: value})
            except IllegalArgumentError:
                assert False

    for key, values in invalid.items():
        for value in values:
            try:
                classname(**{key: value})
                assert False
            except IllegalArgumentError:
                pass
