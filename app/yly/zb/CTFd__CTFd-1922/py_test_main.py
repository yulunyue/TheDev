import flask.helpers
from werkzeug.utils import safe_join

flask.helpers.safe_join = safe_join
import pytest

pytest.main(["--json-report", "tests/admin/test_csv.py"])
