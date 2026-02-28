from common.util.test import TestBase, sys
from common.third_util.py_test_util import pytest

pytestmark = pytest.mark.skipif(sys.platform.startswith("win"), reason="整个模块跳过")
try:
    from common.third_util.io.gunicorn_util import GunicornUtil
except ModuleNotFoundError:
    pass


class TestGunicorn(TestBase):
    def setup_class(self):
        GunicornUtil().start()
