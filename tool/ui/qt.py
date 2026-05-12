from common.tool.toolbase import ToolBase
from common.third_util.pyqt5.stealth_browser import StealthBrowser
from common.tool.export import ProcessLock
import os


class QtTool(ToolBase):
    def main(self):
        lock = ProcessLock("qt")
        if not lock.start_unique():
            return
        lock.set_pid(os.getpid())
        StealthBrowser().exec()


if __name__ == "__main__":
    QtTool().run()
