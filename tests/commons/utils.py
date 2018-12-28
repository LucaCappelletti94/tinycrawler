from tinycrawler import IllegalArgumentError
from typing import List, Callable, Dict
import pytest


def recursive_arguments_test(classname: object, keys: List[str], arguments: Dict, handling: Callable, **kwargs):
    if keys:
        key = keys.pop()
        for value in arguments[key]:
            recursive_arguments_test(
                classname, list(keys), arguments, handling, **{key: value}, **kwargs)
    else:
        handling(classname, **kwargs)


def positive_handling(func: Callable, **kwargs):
    func(**kwargs)


def negative_handling(func: Callable, **kwargs):
    with pytest.raises((AssertionError, IllegalArgumentError)):
        func(**kwargs)


def arguments_test(classname: object, arguments_list: List[Dict], handling: Callable):
    for arguments in arguments_list:
        keys = list(arguments.keys())
        recursive_arguments_test(classname, keys, arguments, handling)


def double_arguments_test(classname: object, valid: List[Dict], invalid: List[Dict]):
    if not isinstance(valid, list):
        valid = [valid]
    if not isinstance(invalid, list):
        invalid = [invalid]

    arguments_test(classname, valid, positive_handling)
    arguments_test(classname, invalid, negative_handling)
