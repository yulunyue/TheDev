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


def wrap_fun(f, f2):

    def wrap(*args, **kw):
        return f2(f, *args, **kw)

    return wrap


def mock_flask():
    from flask import helpers
    from werkzeug.utils import safe_join

    helpers.safe_join = safe_join


def mock_markupsafe():
    import markupsafe

    markupsafe.soft_unicode = lambda a: str(a)


def mock_log():
    import logging

    DEFAULT_FMT = "".join(
        [
            "[%(asctime)s]",
            # "levelname",
            # "process)s:%(threadName",
            "[%(pathname)s:%(lineno)s]",
            "[%(funcName)s]",
            " %(message)s",
        ]
    )

    log_dir = ".log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    class Log(logging.Logger):
        def __init__(self, name, level=0):
            super().__init__(name, level)
            h = logging.FileHandler(
                os.path.join(log_dir, f"{name}.log"),
                mode="w",
            )
            h.setFormatter(DEFAULT_FMT)
            self.addHandler(h)

    def get_log(name="dev"):
        return Log(name)

    logging.getLogger = get_log


class TempFile:
    closed = False

    def __init__(self):
        self.data = b""

    def close(self):
        self.closed = True

    def write(self, data):
        self.data = data

    def read(self):
        return self.data


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
    mock_fun(mock_log)
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
