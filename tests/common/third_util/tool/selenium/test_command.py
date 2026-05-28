from .test_base import SeleniumTestBase


class TestSeleniumCommand(SeleniumTestBase):

    def test_do_cmd_go(self):
        url = self.get_page_url("index.html")
        self.selenium.do_cmd("go", url)
        assert "index.html" in self.selenium.current_url

    def test_do_cmd_path(self):
        url = self.get_page_url("index.html")
        self.selenium.do_cmd("go", url)
        result = self.selenium.do_cmd("path", "//li[@class='list-item']")
        assert "li" in result.lower()
        assert "Item" in result

    def test_do_cmd_click(self):
        url = self.get_page_url("index.html")
        self.selenium.do_cmd("go", url)
        self.selenium.do_cmd("click", "//button[@id='btn-click']")
        msg_box = self.selenium.get_by_id("message-box")
        assert msg_box.is_displayed() is True

    def test_do_cmd_sendkeys(self):
        url = self.get_page_url("form.html")
        self.selenium.do_cmd("go", url)
        self.selenium.do_cmd("sendkeys", "//input[@id='name']", "Test Name")
        input_ele = self.selenium.get_by_id("name")
        assert input_ele.get_attribute("value") == "Test Name"

    def test_do_cmd_id(self):
        url = self.get_page_url("index.html")
        self.selenium.do_cmd("go", url)
        result = self.selenium.do_cmd("id", "title")
        assert "h1" in result.lower()
        assert "Selenium Test Page" in result

    def test_do_cmd_reload(self):
        url = self.get_page_url("index.html")
        self.selenium.do_cmd("go", url)
        self.selenium.driver.execute_script("document.getElementById('title').textContent = 'Changed'")
        self.selenium.do_cmd("reload")
        title = self.selenium.get_by_id("title")
        assert "Selenium Test Page" in title.text

    def test_do_cmd_open(self):
        url = self.get_page_url("window.html")
        self.selenium.do_cmd("go", url)
        self.selenium.do_cmd("open", "//button[@id='btn-open-window']")
        self.selenium.close_current_window()
        self.selenium.switch_to_window(0)

    def test_do_cmds_batch(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        self.selenium.do_cmd("click", "//button[@id='btn-click']")
        msg_box = self.selenium.get_by_id("message-box")
        assert msg_box.is_displayed() is True

    def test_do_cmd_exception(self):
        url = self.get_page_url("index.html")
        self.selenium.do_cmd("go", url)
        result = self.selenium.do_cmd("click", "//element[@id='nonexistent']")
        assert "Message" in result