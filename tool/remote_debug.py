from common.util.export import ToolBase
from common.third_util.debug_py_util import DebugPyUtil


class DebugTool(ToolBase):

    def debug(self):
        DebugPyUtil().run()


if __name__ == "__main__":
    DebugTool().run()
