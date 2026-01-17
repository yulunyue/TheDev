from common.third_util.py_test_util import PyTestUtil
from common.util.export import logger, base64_encode, File, SYS_ARGS
from common.tool.export import PyUtil, ToolBase


class PyTest(ToolBase):
    taget = ["tests"]

    def coverage(self):
        PyTestUtil().set_aim("tests").coverage()

    def test(self, key: str):
        taget = self.taget
        if key:
            name, *args = key.split("::")
            taget = File(self.taget[0]).list_dir(
                depth=8, mathchs=[name], ignores=[".*__pycache__"]
            )
            if args:
                if len(taget) != 1:
                    raise Exception(key, taget)
                taget = ["::".join([taget[0].path] + args)]
            if not taget:
                raise Exception(key)
        PyTestUtil().set_aim(*taget).coverage()


if __name__ == "__main__":
    PyTest().run()
