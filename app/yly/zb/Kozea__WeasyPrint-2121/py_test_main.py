import pytest
import os
import subprocess

PY_MAIN_CMD = "tests/css/test_expanders.py tests/css/test_validation.py tests/layout/test_grid.py"
RESULT_JSON_FILE = "result.json"


def mock_fun(f):
    try:
        f()
    except Exception as e:
        print(f, e)


def mock_flask():
    from flask import helpers
    from werkzeug.utils import safe_join

    helpers.safe_join = safe_join


def mock_markupsafe():
    import markupsafe

    markupsafe.soft_unicode = lambda a: str(a)


class Mock:
    def __init__(self, name, *args, **kw):
        self.name = name
        self.args = args
        self.kw = kw

    def __getattribute__(self, name):
        return self

    def __gt__(self, other):
        return False

    def __call__(self, *args, **kw):
        return self


def mock_cffi():
    import cffi

    class FFIMOCK(cffi.FFI):
        def dlopen(self, *args, **kw):
            try:
                ret = super().dlopen(*args, **kw)
            except Exception as e:
                ret = Mock("cffi.FFI", *args, **kw)
            return ret

    # cffi.FFI = Mock("cffi.FFI")


def mock_py():
    mock_fun(mock_markupsafe)
    mock_fun(mock_flask)
    mock_fun(mock_cffi)


def run_py_test():
    mock_py()
    py_test_args = [f"{v}" for v in PY_MAIN_CMD.split(" ")] + [
        "--json-report",
        f"--json-report-file={RESULT_JSON_FILE}",
    ]
    print(py_test_args)
    pytest.main(py_test_args)


if __name__ == "__main__":
    run_py_test()
