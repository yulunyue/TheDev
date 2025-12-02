import os
import sys

from common.third_util.py_test_util import PyTestUtil
from common.util.export import ToolBase


class PyTestMain(ToolBase):
    def prepare(self, root, **kw):
        self.root = root
        self.u = PyTestUtil().set_root(root)

    def dev(self):
        aim1 = self.root + "/tests/admin/test_csv.py"
        self.u.set_flags(aim1).main()

    def dev1(self):
        aim1 = "tests/test_pytest.py"
        self.u.set_flags(aim1).main()

    def debug(self):
        self.dev()


if __name__ == "__main__":
    PyTestMain().run()
