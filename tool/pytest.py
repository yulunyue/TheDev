from common.third_util.py_test_util import PyTestUtil
from common.util.export import ToolBase, logger, base64_encode, File, SYS_ARGS
from common.tool.export import PyUtil


class PyTest(ToolBase):
    taget = ["tests"]

    def coverage(self):
        PyTestUtil().set_aim("tests").coverage()

    def run(self):
        taget = self.taget
        if SYS_ARGS:
            taget = File(self.taget[0]).list_dir(
                depth=8,
                filter=lambda v: "__pycache__" not in v.path and SYS_ARGS[0] in v.path,
            )
            if not taget:
                raise Exception(SYS_ARGS[0])
        PyTestUtil().set_aim(*taget).main()


if __name__ == "__main__":
    PyTest().run()
