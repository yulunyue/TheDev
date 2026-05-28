from selenium.webdriver.remote.webelement import WebElement
from .test_base import SeleniumTestBase


class TestSeleniumElement(SeleniumTestBase):

    def test_get_by_id(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        ele = self.selenium.get_by_id("title")
        assert isinstance(ele, WebElement)
        assert "Selenium Test Page" in ele.text

    def test_get_by_xpath(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        ele = self.selenium.get_by_xpath("//h1[@id='title']")
        assert isinstance(ele, WebElement)
        assert "Selenium Test Page" in ele.text

    def test_get_by_tag(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        ele = self.selenium.get_by_tag("h1")
        assert isinstance(ele, WebElement)

    def test_get_clickable(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        ele = self.selenium.get_clickable("//button[@id='btn-click']")
        assert isinstance(ele, WebElement)
        assert ele.is_enabled()

    def test_get_elements_by_xpath(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        eles = self.selenium.get_elements_by_xpath("//li[@class='list-item']")
        assert len(eles) == 3
        for ele in eles:
            assert isinstance(ele, WebElement)

    def test_find_by_xpath(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        eles = self.selenium.find_by_xpath("//p[@class='text-para']")
        assert len(eles) == 2

    def test_find_by_tag(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        eles = self.selenium.find_by_tag("button")
        assert len(eles) >= 2

    def test_find_by_tag_with_text(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        eles = self.selenium.find_by_tag("li")
        eles_with_text = [e for e in eles if "Item 1" in e.text]
        assert len(eles_with_text) >= 1

    def test_find_by_text(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        eles = self.selenium.find_by_xpath("//li[@class='list-item']")
        eles_with_text = [e for e in eles if "Item 2" in e.text]
        assert len(eles_with_text) >= 1

    def test_get_children(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        parent = self.selenium.get_by_xpath("//ul[@id='list-items']")
        children = self.selenium.get_children(parent)
        assert len(children) >= 3

    def test_dfs(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        parent = self.selenium.get_by_xpath("//div[@class='parent']")
        visited = []

        def collect(ele, paths=None):
            visited.append(ele.tag_name)

        self.selenium.dfs(parent, collect)
        assert len(visited) >= 2