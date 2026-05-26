class SeleniumCommand:
    def __init__(self, driver, page, element, script, cookie):
        self.driver = driver
        self.page = page
        self.element = element
        self.script = script
        self.cookie = cookie

    def do_cmd(self, method, *args):
        try:
            if method == "go":
                return self.page.get(*args)
            elif method == "path":
                return self.script.e_format(self.element.get_elements_by_xpath(args[0]))
            elif method == "click":
                return self.element.get_by_xpath(args[0]).click()
            elif method == "open":
                self.element.get_by_xpath(args[0]).click()
                self.driver.wait_for_window()
                self.driver.switch_to_window()
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
                return self.cookie.get_cookies(name=name)
            return "todo"
        except Exception as e:
            return str(e)

    def do_cmds(self, *args):
        for a in args:
            self.do_cmd(a)