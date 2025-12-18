import os

os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"
import subprocess
import sys

import pytest
import socket

socket.setdefaulttimeout(1)

PY_MAIN_CMD = "%{PY_MAIN_CMD}"
PY_TEST_RESULT_JSON_FILE = "%{PY_TEST_RESULT_JSON_FILE}"
sys.path.insert(0, "src")


def mock_fun(f):
    try:
        f()
    except Exception as e:
        pass


def wrap_fun(f, default_value=""):

    def wrap(*args, **kw):
        ret = default_value
        try:
            ret = f()
            if callable(default_value):
                return default_value(ret)
        except Exception as e:
            pass
        return ret

    return wrap


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


def mock_importlib():
    from importlib import metadata

    metadata.version = wrap_fun(metadata.version, default_value="0.0.0")


def mock_platform():
    import platform

    def util(v):
        a, b, c = v
        if not a:
            a = "0.0.0"
        return a, b, c

    platform.mac_ver = wrap_fun(platform.mac_ver, default_value=util)


def mock_py():
    mock_fun(mock_markupsafe)
    mock_fun(mock_flask)
    mock_fun(mock_platform)
    # mock_fun(mock_cffi)
    # mock_fun(mock_importlib)


def run_py_test():
    mock_py()
    py_test_args = [f"{v}" for v in PY_MAIN_CMD.split(" ")] + [
        "--json-report",
        f"--json-report-file={PY_TEST_RESULT_JSON_FILE}",
    ]
    print(" ".join(py_test_args))
    pytest.main(py_test_args)


if __name__ == "__main__":
    run_py_test()
