import os
import sys

from common.third_util.py_test_util import PyTestUtil
from common.util.export import ToolBase


class PyTestMain(ToolBase):
    def prepare(self, root, aim, **kw):
        self.root = root
        self.u = PyTestUtil().set_aim(aim).set_root(root)

    def main(self):
        self.u.main()

    def cover(self):
        self.u.coverage()

    def dev(self):
        self.main()

    def debug(self):
        self.dev()


if __name__ == "__main__":
    PyTestMain().run()
