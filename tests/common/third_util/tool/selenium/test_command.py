from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .test_base import SeleniumTestBase


class TestSeleniumCommand(SeleniumTestBase):

    def test_navigation_chain(self):
        url1 = self.get_page_url("index.html")
        url2 = self.get_page_url("form.html")
        self.driver.get(url1)
        assert "index.html" in self.driver.current_url
        self.driver.get(url2)
        assert "form.html" in self.driver.current_url

    def test_click_and_verify(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='btn-click']")))
        btn.click()
        msg_box = self.driver.find_element(By.ID, "message-box")
        assert msg_box.is_displayed() is True

    def test_send_keys(self):
        url = self.get_page_url("form.html")
        self.driver.get(url)
        input_ele = self.wait.until(EC.presence_of_element_located((By.ID, "name")))
        input_ele.clear()
        input_ele.send_keys("Test Name")
        assert input_ele.get_attribute("value") == "Test Name"

    def test_find_and_get_text(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        title = self.wait.until(EC.presence_of_element_located((By.ID, "title")))
        assert "Selenium Test Page" in title.text

    def test_reload_page(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        self.driver.execute_script("document.getElementById('title').textContent = 'Changed'")
        self.driver.refresh()
        title = self.driver.find_element(By.ID, "title")
        assert "Selenium Test Page" in title.text

    def test_get_cookies_dict(self):
        self.driver.get("about:blank")
        cookies = self.driver.get_cookies()
        assert isinstance(cookies, list)