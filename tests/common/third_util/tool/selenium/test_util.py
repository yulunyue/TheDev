from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from .test_base import SeleniumTestBase


class TestSeleniumUtil(SeleniumTestBase):

    def test_full_workflow(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        title = self.selenium.get_by_id("title")
        assert isinstance(title, WebElement)
        assert "Selenium Test Page" in title.text
        btn = self.selenium.get_clickable("//button[@id='btn-click']")
        btn.click()
        msg_box = self.selenium.get_by_id("message-box")
        assert msg_box.is_displayed() is True
        self.selenium.reload()
        msg_box = self.selenium.get_by_id("message-box")
        assert msg_box.is_displayed() is False

    def test_chain_navigation(self):
        url1 = self.get_page_url("index.html")
        url2 = self.get_page_url("form.html")
        self.selenium.get(url1).get(url2)
        assert "form.html" in self.selenium.current_url

    def test_property_access(self):
        assert self.selenium.element is not None
        assert self.selenium.page is not None
        assert self.selenium.window is not None
        assert self.selenium.script is not None
        assert self.selenium.command is not None

    def test_form_interaction(self):
        url = self.get_page_url("form.html")
        self.selenium.get(url)
        name_input = self.selenium.get_by_id("name")
        name_input.send_keys("John Doe")
        assert name_input.get_attribute("value") == "John Doe"
        email_input = self.selenium.get_by_id("email")
        email_input.send_keys("john@example.com")
        assert email_input.get_attribute("value") == "john@example.com"
        gender_select = self.selenium.get_by_xpath("//select[@id='gender']")
        select = Select(gender_select)
        select.select_by_value("male")
        assert select.first_selected_option.get_attribute("value") == "male"
        checkbox = self.selenium.get_by_id("agree")
        checkbox.click()
        assert checkbox.is_selected() is True

    def test_list_items(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        items = self.selenium.get_elements_by_xpath("//li[@class='list-item']")
        texts = [item.text for item in items]
        assert texts == ["Item 1", "Item 2", "Item 3"]

    def test_nested_elements(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        parent = self.selenium.get_by_xpath("//div[@class='parent']")
        children = self.selenium.get_children(parent)
        assert len(children) >= 2
        grandchild = self.selenium.get_by_xpath("//span[@class='grandchild']")
        assert grandchild.text in ["Nested Span 1", "Nested Span 2"]

    def test_hidden_element(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        hidden = self.selenium.get_by_id("hidden-span")
        assert hidden.is_displayed() is False
        assert hidden.get_attribute("textContent") == "Hidden Element"

    def test_disabled_button(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        disabled_btn = self.selenium.get_by_id("btn-disabled")
        assert disabled_btn.is_enabled() is False

    def test_current_url_property(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        current = self.selenium.current_url
        assert "index.html" in current
        assert current.startswith("http://")