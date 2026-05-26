from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from .driver import SeleniumDriver
from .element import SeleniumElement
from .page import SeleniumPage
from .window import SeleniumWindow
from .cookie import SeleniumCookie
from .script import SeleniumScript
from .command import SeleniumCommand
from .config import SeleniumConfig


class SeleniumUtil(SeleniumDriver):
    _element: SeleniumElement = None
    _page: SeleniumPage = None
    _window: SeleniumWindow = None
    _cookie: SeleniumCookie = None
    _script: SeleniumScript = None
    _command: SeleniumCommand = None

    def __init__(self, dev_port=9527, default_timeout=6, bypass_proxy=False, auto_start=True):
        super().__init__(dev_port, default_timeout, bypass_proxy, auto_start)

    def load(self):
        super().load()
        self._element = SeleniumElement(self.driver, self.wait)
        self._page = SeleniumPage(self.driver, self.wait)
        self._window = SeleniumWindow(self.driver, self.wait)
        self._cookie = SeleniumCookie(self.driver)
        self._script = SeleniumScript(self.driver)
        self._command = SeleniumCommand(self.driver, self._page, self._element, self._script, self._cookie)
        return self

    def get_by_id(self, key):
        return self._element.get_by_id(key)

    def get_by_xpath(self, key):
        return self._element.get_by_xpath(key)

    def get_by_tag(self, key):
        return self._element.get_by_tag(key)

    def get_clickable(self, key):
        return self._element.get_clickable(key)

    def get_elements_by_xpath(self, key):
        return self._element.get_elements_by_xpath(key)

    def find_by_xpath(self, xpath):
        return self._element.find_by_xpath(xpath)

    def find_by_tag(self, name, **kw):
        return self._element.find_by_tag(name, **kw)

    def find_by_text(self, eles, text=None):
        return self._element.find_by_text(eles, text)

    def get_children(self, e):
        return self._element.get_children(e)

    def dfs(self, e, call, parents=None):
        return self._element.dfs(e, call, parents)

    def get(self, url):
        return self._page.get(url)

    def reload(self):
        return self._page.reload()

    def wait_url_contains(self, key):
        return self._page.wait_url_contains(key)

    def wait_url_is(self, url, timeout=None):
        return self._page.wait_url_is(url, timeout)

    def wait_todo(self, f, timeout=None):
        return self._page.wait_todo(f, timeout)

    def wait_until(self, func=None, timeout=120, wait_time=0.2):
        return self._page.wait_until(func, timeout, wait_time)

    def wait_for_window(self):
        return self._window.wait_for_window()

    def switch_to_window(self, idx=-1):
        return self._window.switch_to_window(idx)

    def close_current_window(self):
        return self._window.close_current_window()

    def get_cookies(self, name=None):
        return self._cookie.get_cookies(name)

    def scroll_into_view(self, ele):
        return self._script.scroll_into_view(ele)

    def script_click(self, ele):
        return self._script.script_click(ele)

    def get_xpath_from_devtools(self, element):
        return self._script.get_xpath_from_devtools(element)

    def e_format(self, element, text_max_size=20):
        return self._script.e_format(element, text_max_size)

    def do_cmd(self, method, *args):
        return self._command.do_cmd(method, *args)

    def do_cmds(self, *args):
        return self._command.do_cmds(*args)

    @property
    def current_url(self):
        return self.driver.current_url


__all__ = ["SeleniumUtil", "SeleniumConfig", "By", "WebElement"]