from common.third_util.py_test_util import PyTestUtil
from common.util.export import ToolBase, logger, base64_encode
from common.tool.export import PyUtil


class PyTes(ToolBase):
    def coverage(self):
        PyTestUtil().set_aim("tests").coverage()

    def pip_download(self, pkg):
        d = PyUtil().pip_download(pkg)
        logger.info(d)

    def b64_encode(self, code="print('hello world')"):
        logger.info(base64_encode(code))


if __name__ == "__main__":
    PyTes().run()
