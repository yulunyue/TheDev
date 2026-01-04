from common.third_util.py_test_util import PyTestUtil
from common.util.export import ToolBase, logger
from common.tool.export import PyUtil


class PyTestMain(ToolBase):
    def coverage(self):
        PyTestUtil().set_aim("tests").coverage()

    def pip_download(self, pkg):
        d = PyUtil().pip_download(pkg)
        logger.info(d)


if __name__ == "__main__":
    PyTestMain().run()
