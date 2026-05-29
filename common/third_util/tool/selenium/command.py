from typing import Any, Optional, Dict, Union


class SeleniumCommand:
    """命令模式封装，支持链式调用"""

    def __init__(self, driver, page, element, script):
        self.driver = driver
        self.page = page
        self.element = element
        self.script = script

    def do_cmd(self, method: str, *args) -> Any:
        """
        执行单个命令。

        Args:
            method: 命令名称
            args: 命令参数

        Returns:
            命令执行结果
        """
        try:
            if method == "go":
                return self.page.get(*args)
            elif method == "path":
                return self.script.e_format(self.element.get_elements_by_xpath(args[0]))
            elif method == "click":
                return self.element.get_by_xpath(args[0]).click()
            elif method == "open":
                self.element.get_by_xpath(args[0]).click()
                self.page.wait_for_window()
                self.page.switch_to_window()
                return self.driver.current_url
            elif method == "reload":
                return self.page.reload()
            elif method == "sendkeys":
                r = self.element.get_by_xpath(args[0])
                r.clear()
                return r.send_keys(args[1])
            elif method == "id":
                return self.script.e_format(self.element.get_by_id(args[0]))
            elif method == "get_cookies":
                name = None if len(args) == 0 else args[0]
                return self.driver.get_cookies(name)
            return "todo"
        except Exception as e:
            return str(e)

    def do_cmds(self, *args) -> None:
        """批量执行命令"""
        for a in args:
            self.do_cmd(a)
