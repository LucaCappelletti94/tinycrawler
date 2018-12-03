"""Test for version file syntax."""
from tinycrawler.process.process_handler import ProcessHandler
from inspect import signature


def test_exceptions():
    p = ProcessHandler(None, None, None)
    methods = [
        p._enough,
        p._target,
        p._get_job
    ]
    passed = False
    for m in methods:
        try:
            m(*[None for i in range(len(signature(m).parameters))])
            passed = True
        except NotImplementedError:
            pass

    assert not passed
