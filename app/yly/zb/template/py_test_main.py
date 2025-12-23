import os
import pytest

PY_MAIN_CMD = "%{PY_MAIN_CMD}"
PY_TEST_RESULT_JSON_FILE = "%{PY_TEST_RESULT_JSON_FILE}"


def run_py_test():
    py_test_args = [f"{v}" for v in PY_MAIN_CMD.split(" ")] + [
        "--json-report",
        f"--json-report-file={PY_TEST_RESULT_JSON_FILE}",
    ]
    print(" ".join(py_test_args))
    pytest.main(py_test_args)


if __name__ == "__main__":
    run_py_test()
