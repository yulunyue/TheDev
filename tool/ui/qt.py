from common.tool.toolbase import ToolBase
from common.third_util.pyqt5.stealth_browser import StealthBrowser
from common.tool.export import ProcessLock


class QtTool(ToolBase):
    def main(self):
        if not ProcessLock("qt").start_unique():
            return
        StealthBrowser().exec()


if __name__ == "__main__":
    QtTool().run()
