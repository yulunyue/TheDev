from common.third_util.selenium_util import SeleniumUtil, By, WebElement
from common.util.export import time, logger, ToolBase


class WebTool(ToolBase):
    def prepare(self):
        self.s = SeleniumUtil().load()
        return self

    def do_cmd(self, *args):
        return self.s.do_cmd(*args)


if __name__ == "__main__":
    WebTool().run()
