from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from .test_base import SeleniumTestBase, CHROME_BIN_PATH, CHROMEDRIVER_PATH


class TestSeleniumDriver(SeleniumTestBase):

    def test_load_headless_success(self):
        assert self.driver is not None
        assert self.wait is not None
        assert self.options is not None

    def test_driver_type(self):
        from selenium.webdriver.chrome.webdriver import WebDriver
        assert isinstance(self.driver, WebDriver)
        assert isinstance(self.wait, WebDriverWait)

    def test_get_cookies_empty(self):
        self.driver.get("about:blank")
        cookies = self.driver.get_cookies()
        assert isinstance(cookies, list)

    def test_get_cookies_with_name(self):
        self.driver.get("about:blank")
        cookie = {c["name"]: c["value"] for c in self.driver.get_cookies()}
        assert cookie.get("nonexistent") is None

    def test_quit(self):
        options = Options()
        options.binary_location = CHROME_BIN_PATH
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        service = Service(executable_path=CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)
        assert driver is not None
        driver.quit()

    def test_current_url(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        assert "index.html" in self.driver.current_url