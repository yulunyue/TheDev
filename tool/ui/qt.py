from common.tool.toolbase import ToolBase
from common.third_util.pyqt5.stealth_browser import StealthBrowser


class QtTool(ToolBase):
    def main(self):
        StealthBrowser().exec()


if __name__ == "__main__":
    QtTool().run()
