from common.third_util.tool.selenium_util import SeleniumUtil, By, WebElement
from common.util.export import time, logger
from common.tool.export import ToolBase


class WebTool(ToolBase):

    def dev(self, *args):
        s = SeleniumUtil().load()
        self.cli(s.do_cmd)


if __name__ == "__main__":
    WebTool().run()
