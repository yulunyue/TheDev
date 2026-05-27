from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from .test_base import SeleniumTestBase


class TestSeleniumScript(SeleniumTestBase):

    def test_scroll_into_view(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        target = self.wait.until(EC.presence_of_element_located((By.ID, "scroll-target")))
        self.driver.execute_script("arguments[0].scrollIntoView();", target)
        location = target.location
        viewport_height = self.driver.execute_script("return window.innerHeight")
        assert location["y"] < viewport_height

    def test_script_click(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        btn = self.wait.until(EC.presence_of_element_located((By.ID, "btn-click")))
        msg_box = self.driver.find_element(By.ID, "message-box")
        assert msg_box.is_displayed() is False
        self.driver.execute_script("arguments[0].click();", btn)
        msg_box = self.driver.find_element(By.ID, "message-box")
        assert msg_box.is_displayed() is True

    def test_execute_script_return_value(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        result = self.driver.execute_script("return document.title")
        assert result == "Selenium Test Page"

    def test_get_xpath_js(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        ele = self.driver.find_element(By.ID, "title")
        js_code = """
        function getXPathForElement(element) {
            const idx = (sib, name) => sib 
                ? idx(sib.previousElementSibling, name||sib.localName) + (sib.localName == name)
                : 1;
            const segs = elm => !elm || elm.nodeType !== 1 
                ? ['']
                : elm.id && document.getElementById(elm.id) === elm
                    ? [`//*[@id="${elm.id}"]`]
                    : [...segs(elm.parentNode), `${elm.localName.toLowerCase()}[${idx(elm)}]`];
            return segs(element).join('/');
        }
        return getXPathForElement(arguments[0]);
        """
        xpath = self.driver.execute_script(js_code, ele)
        assert "title" in xpath or "h1" in xpath.lower()

    def test_wait_doc_ready(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        state = self.driver.execute_script("return document.readyState")
        assert state == "complete"