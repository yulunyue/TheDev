from common.third_util.tool.selenium import SeleniumUtil, By, WebElement, BrowerUser
from common.util.export import time, logger
from common.tool.export import ToolBase
import sys


class WebTool(ToolBase):
    def __init__(self) -> None:
        super().__init__()
        self.s = SeleniumUtil(mode="lc").load()

    def do_cmd(self, *args):
        return self.s.do_cmd(*args)

    def brower(self):
        BrowerUser().start()


if __name__ == "__main__":
    WebTool().run()
