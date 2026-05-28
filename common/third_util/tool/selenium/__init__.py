from typing import Union, Optional, Dict, List, Callable, Any
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from .driver import SeleniumDriver, Request
from .element import SeleniumElement
from .page import SeleniumPage, SeleniumWindow
from .script import SeleniumScript
from .command import SeleniumCommand
from .config import SeleniumConfig
from .browser_user import BrowerUser


class SeleniumUtil(SeleniumDriver):
    """
    Selenium 工具门面类，整合所有子模块功能。

    模式说明：
    - int: 调试模式，连接已有 Chrome 实例的端口
    - "headless": 无头模式，独立启动 Chrome
    - 其他字符串: 独立实例模式，使用独立的 user-data 目录
    """

    _element: SeleniumElement = None
    _page: SeleniumPage = None
    _window: SeleniumWindow = None
    _script: SeleniumScript = None
    _command: SeleniumCommand = None

    def load(self) -> "SeleniumUtil":
        super().load()
        self._element = SeleniumElement(self.driver, self.wait)
        self._page = SeleniumPage(self, self.wait)
        self._window = SeleniumWindow(self.driver, self.wait)
        self._script = SeleniumScript(self.driver)
        self._command = SeleniumCommand(
            self.driver, self._page, self._element, self._script, self._window
        )
        return self

    @property
    def element(self) -> SeleniumElement:
        return self._element

    @property
    def page(self) -> SeleniumPage:
        return self._page

    @property
    def window(self) -> SeleniumWindow:
        return self._window

    @property
    def script(self) -> SeleniumScript:
        return self._script

    @property
    def command(self) -> SeleniumCommand:
        return self._command

    def get_by_id(self, key: str) -> WebElement:
        return self._element.get_by_id(key)

    def get_by_xpath(self, key: str) -> WebElement:
        return self._element.get_by_xpath(key)

    def get_by_tag(self, key: str) -> WebElement:
        return self._element.get_by_tag(key)

    def get_clickable(self, key: str) -> WebElement:
        return self._element.get_clickable(key)

    def get_elements_by_xpath(self, key: str) -> List[WebElement]:
        return self._element.get_elements_by_xpath(key)

    def find_by_xpath(self, xpath: str) -> List[WebElement]:
        return self._element.find_by_xpath(xpath)

    def find_by_tag(self, name: str, **kw) -> List[WebElement]:
        return self._element.find_by_tag(name, **kw)

    def find_by_text(
        self, eles: List[WebElement], text: Optional[str] = None
    ) -> List[WebElement]:
        return self._element.find_by_text(eles, text)

    def get_children(self, e: WebElement) -> List[WebElement]:
        return self._element.get_children(e)

    def dfs(self, e: WebElement, call: Callable, parents: Optional[List] = None):
        return self._element.dfs(e, call, parents)

    def get(self, url: str) -> "SeleniumUtil":
        self._page.get(url)
        return self

    def reload(self) -> "SeleniumUtil":
        self._page.reload()
        return self

    def wait_url_contains(self, key: str) -> None:
        self._page.wait_url_contains(key)

    def wait_url_is(self, url: str, timeout: Optional[int] = None) -> None:
        self._page.wait_url_is(url, timeout)

    def wait_todo(self, f, timeout: Optional[int] = None) -> None:
        self._page.wait_todo(f, timeout)

    def wait_until(
        self,
        func: Optional[Callable[[], Any]] = None,
        timeout: int = 120,
        wait_time: float = 0.2,
    ) -> Any:
        return self._page.wait_until(func, timeout, wait_time)

    def wait_for_window(self) -> Optional[str]:
        return self._window.wait_for_window()

    def switch_to_window(self, idx: int = -1) -> Optional[str]:
        return self._window.switch_to_window(idx)

    def close_current_window(self) -> None:
        self._window.close_current_window()

    def get_cookies(
        self, name: Optional[str] = None
    ) -> Union[Dict[str, str], str, None]:
        return super().get_cookies(name)

    def scroll_into_view(self, ele: WebElement) -> None:
        self._script.scroll_into_view(ele)

    def script_click(self, ele: WebElement) -> None:
        self._script.script_click(ele)

    def get_xpath_from_devtools(self, element: WebElement) -> str:
        return self._script.get_xpath_from_devtools(element)

    def e_format(self, element: WebElement, text_max_size: int = 20) -> str:
        return self._script.e_format(element, text_max_size)

    def do_cmd(self, method: str, *args) -> Any:
        return self._command.do_cmd(method, *args)

    def do_cmds(self, *args) -> None:
        self._command.do_cmds(*args)

    @property
    def current_url(self) -> str:
        return self.driver.current_url


__all__ = [
    "SeleniumUtil",
    "SeleniumDriver",
    "SeleniumConfig",
    "SeleniumElement",
    "SeleniumPage",
    "SeleniumWindow",
    "SeleniumScript",
    "SeleniumCommand",
    "By",
    "WebElement",
]
