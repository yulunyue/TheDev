from common.util.export import ToolBase, File, logger
from common.tool.export import OsUtil
from .constant import C


class PyBuildTool(ToolBase):
    def build(self, path):
        self.root = File(path)
        self.target = File(
            f"{C.OUT_PUT_DIR}/{self.root.name}{C.BIN_SUFFIX}"
        ).make_dir_if_not_exist()
        ret = OsUtil(C.GCC).run(
            self.root.path, C.DEBUG_FLAG, C.O_FLAG, self.target.path
        )
        logger.info(ret)

    def execute(self, path, *args):
        self.build(path)
        ret = OsUtil(self.target.path).run(*args)
        logger.info(ret)


if __name__ == "__main__":
    PyBuildTool().run()
