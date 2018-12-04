"""Test for version file syntax."""
from tinycrawler.process.process_handler import ProcessHandler
from multiprocessing.managers import RemoteError
from tinycrawler.managers import TinyCrawlerManager
from inspect import signature


def test_exceptions():
    p = ProcessHandler(None, None, None)
    t = TinyCrawlerManager()
    t.start()
    methods = [
        p._enough,
        p._target,
        p._get_job,
        t.Local,
        t.Log,
        t.Robots,
        t.Urls,
        t.Statistics
    ]
    passed = False
    for m in methods:

        try:
            m(*[None for i in range(len(signature(m).parameters))])
            passed = True
        except NotImplementedError:
            pass
        except RemoteError as e:
            print(m.__name__)
            print(signature(m))
            print(signature(m).parameters)
            raise e

    assert not passed
