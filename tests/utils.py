from tinycrawler.exceptions import IllegalArgumentError


def arguments_test(classname, valid, invalid):
    for key, values in valid.items():
        for value in values:
            try:
                classname(**{key: value})
            except IllegalArgumentError:
                print("Argument {arg} of class {classname} raised IllegalArgumentError with value {value}.".format(
                    arg=key, classname=classname.__name__, value=value))
                assert False

    for key, values in invalid.items():
        for value in values:
            try:
                classname(**{key: value})
                print("Argument {arg} of class {classname} did not raise IllegalArgumentError with value {value}.".format(
                    arg=key, classname=classname.__name__, value=value))
                assert False
            except IllegalArgumentError:
                pass
