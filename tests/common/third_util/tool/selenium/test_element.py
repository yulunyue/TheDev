from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from .test_base import SeleniumTestBase


class TestSeleniumElement(SeleniumTestBase):

    def test_get_by_id(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        ele = self.wait.until(EC.presence_of_element_located((By.ID, "title")))
        assert isinstance(ele, WebElement)
        assert "Selenium Test Page" in ele.text

    def test_get_by_xpath(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        ele = self.wait.until(EC.presence_of_element_located((By.XPATH, "//h1[@id='title']")))
        assert isinstance(ele, WebElement)
        assert "Selenium Test Page" in ele.text

    def test_get_by_tag(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        ele = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        assert isinstance(ele, WebElement)

    def test_get_clickable(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        ele = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='btn-click']")))
        assert isinstance(ele, WebElement)
        assert ele.is_enabled()

    def test_get_elements_by_xpath(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//li[@class='list-item']")))
        eles = self.driver.find_elements(By.XPATH, "//li[@class='list-item']")
        assert len(eles) == 3
        for ele in eles:
            assert isinstance(ele, WebElement)

    def test_find_by_xpath(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        eles = self.driver.find_elements(By.XPATH, "//p[@class='text-para']")
        assert len(eles) == 2

    def test_find_by_tag(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        eles = self.driver.find_elements(By.TAG_NAME, "button")
        assert len(eles) >= 2

    def test_find_by_tag_with_text(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        eles = self.driver.find_elements(By.TAG_NAME, "li")
        filtered = [e for e in eles if "Item 1" in e.text]
        assert len(filtered) == 1
        assert "Item 1" in filtered[0].text

    def test_get_children(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        parent = self.driver.find_element(By.XPATH, "//ul[@id='list-items']")
        children = parent.find_elements(By.XPATH, ".//*")
        assert len(children) >= 3

    def test_nested_elements(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        parent = self.driver.find_element(By.XPATH, "//div[@class='parent']")
        children = parent.find_elements(By.XPATH, ".//*")
        assert len(children) >= 2