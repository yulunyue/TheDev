from common.third_util.tool.selenium_util import SeleniumUtil, By, WebElement
from common.util.export import time, logger
from common.tool.export import ToolBase
import sys


class WebTool(ToolBase):
    def __init__(self) -> None:
        super().__init__()
        self.s = SeleniumUtil(dev_port="lc").load()

    def do_cmd(self, *args):
        return self.s.do_cmd(*args)


if __name__ == "__main__":
    WebTool().cli(sys.argv[1])
