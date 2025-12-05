import os
import sys

from common.third_util.py_test_util import PyTestUtil
from common.util.export import ToolBase


class PyTestMain(ToolBase):
    def prepare(self, root, **kw):
        self.root = root
        self.u = PyTestUtil().set_root(root)

    def dev(self, test_path="tests"):
        self.u.set_flags(test_path).main()

    def debug(self):
        self.dev()


if __name__ == "__main__":
    PyTestMain().run()
