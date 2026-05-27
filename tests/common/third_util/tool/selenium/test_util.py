from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from .test_base import SeleniumTestBase


class TestSeleniumUtil(SeleniumTestBase):

    def test_full_workflow(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        title = self.wait.until(EC.presence_of_element_located((By.ID, "title")))
        assert isinstance(title, WebElement)
        assert "Selenium Test Page" in title.text
        btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='btn-click']")))
        btn.click()
        msg_box = self.driver.find_element(By.ID, "message-box")
        assert msg_box.is_displayed() is True
        self.driver.refresh()
        msg_box = self.driver.find_element(By.ID, "message-box")
        assert msg_box.is_displayed() is False

    def test_chain_navigation(self):
        url1 = self.get_page_url("index.html")
        url2 = self.get_page_url("form.html")
        self.driver.get(url1)
        self.driver.get(url2)
        assert "form.html" in self.driver.current_url

    def test_form_interaction(self):
        url = self.get_page_url("form.html")
        self.driver.get(url)
        name_input = self.wait.until(EC.presence_of_element_located((By.ID, "name")))
        name_input.send_keys("John Doe")
        assert name_input.get_attribute("value") == "John Doe"
        email_input = self.driver.find_element(By.ID, "email")
        email_input.send_keys("john@example.com")
        assert email_input.get_attribute("value") == "john@example.com"
        gender_select = self.driver.find_element(By.ID, "gender")
        select = Select(gender_select)
        select.select_by_value("male")
        assert select.first_selected_option.get_attribute("value") == "male"
        checkbox = self.driver.find_element(By.ID, "agree")
        checkbox.click()
        assert checkbox.is_selected() is True

    def test_list_items(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//li[@class='list-item']")))
        items = self.driver.find_elements(By.XPATH, "//li[@class='list-item']")
        texts = [item.text for item in items]
        assert texts == ["Item 1", "Item 2", "Item 3"]

    def test_nested_elements(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        parent = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='parent']")))
        children = parent.find_elements(By.XPATH, ".//*")
        assert len(children) >= 2
        grandchild = self.driver.find_element(By.XPATH, "//span[@class='grandchild']")
        assert grandchild.text in ["Nested Span 1", "Nested Span 2"]

    def test_hidden_element(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        hidden = self.wait.until(EC.presence_of_element_located((By.ID, "hidden-span")))
        assert hidden.is_displayed() is False
        assert hidden.text == "Hidden Element"

    def test_disabled_button(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        disabled_btn = self.wait.until(EC.presence_of_element_located((By.ID, "btn-disabled")))
        assert disabled_btn.is_enabled() is False

    def test_current_url_property(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        current = self.driver.current_url
        assert "index.html" in current
        assert current.startswith("file:///")