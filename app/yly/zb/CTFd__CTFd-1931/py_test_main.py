import pytest
import os
import subprocess

PY_MAIN_CMD = "tests/api/v1/test_config.py"
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


def mock_py():
    mock_fun(mock_markupsafe)
    mock_fun(mock_flask)


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
