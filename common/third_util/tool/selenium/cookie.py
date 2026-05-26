class SeleniumCookie:
    def __init__(self, driver):
        self.driver = driver

    def get_cookies(self, name=None):
        cookies = self.driver.get_cookies()
        ret = dict()
        for c in cookies:
            if name is not None and c["name"] == name:
                return c["value"]
            ret[c["name"]] = c["value"]
        return ret