from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from common.third_util.tool.selenium import SeleniumUtil
from .test_base import SeleniumTestBase


class TestSeleniumDriver(SeleniumTestBase):

    def test_load_headless_success(self):
        assert self.selenium.driver is not None
        assert self.selenium.wait is not None
        assert self.selenium.options is not None

    def test_driver_type(self):
        assert isinstance(self.selenium.driver, WebDriver)
        assert isinstance(self.selenium.wait, WebDriverWait)

    def test_get_cookies_empty(self):
        self.selenium.get("about:blank")
        cookies = self.selenium.get_cookies()
        assert isinstance(cookies, dict)

    def test_get_cookies_with_name(self):
        self.selenium.get("about:blank")
        cookie = self.selenium.get_cookies("nonexistent")
        assert cookie is None

    def test_quit(self):
        import pytest
        pytest.skip("headless 模式下创建第二个 Chrome 实例会 crash，跳过")

    def test_current_url(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        assert "index.html" in self.selenium.current_url