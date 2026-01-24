import pytest
import os

PY_MAIN_CMD = os.environ.get("ZB_PY_MAIN_CMD", "%{PY_MAIN_CMD}")
pytest.main(PY_MAIN_CMD.split(" "))
