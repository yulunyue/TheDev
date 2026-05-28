from selenium.webdriver.remote.webelement import WebElement
from .test_base import SeleniumTestBase


class TestSeleniumScript(SeleniumTestBase):

    def test_scroll_into_view(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        target = self.selenium.get_by_id("scroll-target")
        self.selenium.scroll_into_view(target)
        location = target.location
        viewport_height = self.selenium.driver.execute_script("return window.innerHeight")
        assert location["y"] < viewport_height

    def test_script_click(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        btn = self.selenium.get_by_id("btn-click")
        msg_box = self.selenium.get_by_id("message-box")
        assert msg_box.is_displayed() is False
        self.selenium.script_click(btn)
        msg_box = self.selenium.get_by_id("message-box")
        assert msg_box.is_displayed() is True

    def test_get_xpath_from_devtools(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        ele = self.selenium.get_by_id("title")
        xpath = self.selenium.get_xpath_from_devtools(ele)
        assert "title" in xpath or "h1" in xpath.lower()

    def test_e_format_single(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        ele = self.selenium.get_by_id("btn-click")
        formatted = self.selenium.e_format(ele)
        assert "button" in formatted.lower()
        assert "btn-click" in formatted

    def test_e_format_list(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        eles = self.selenium.get_elements_by_xpath("//li[@class='list-item']")
        formatted = self.selenium.e_format(eles)
        assert "Item 1" in formatted
        assert "Item 2" in formatted
        assert "Item 3" in formatted

    def test_wait_doc_ready(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        self.selenium.script.wait_doc_ready(self.selenium.wait)
        state = self.selenium.driver.execute_script("return document.readyState")
        assert state == "complete"