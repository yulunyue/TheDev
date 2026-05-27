from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .test_base import SeleniumTestBase


class TestSeleniumPage(SeleniumTestBase):

    def test_get_new_url(self):
        url1 = self.get_page_url("index.html")
        url2 = self.get_page_url("form.html")
        self.driver.get(url1)
        assert "index.html" in self.driver.current_url
        self.driver.get(url2)
        assert "form.html" in self.driver.current_url

    def test_get_same_url_reload(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        self.driver.execute_script("document.getElementById('title').textContent = 'Modified'")
        title = self.driver.find_element(By.ID, "title")
        assert title.text == "Modified"
        self.driver.get(url)
        title = self.driver.find_element(By.ID, "title")
        assert "Selenium Test Page" in title.text

    def test_reload(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        self.driver.execute_script("document.getElementById('title').textContent = 'Changed'")
        self.driver.refresh()
        title = self.driver.find_element(By.ID, "title")
        assert "Selenium Test Page" in title.text

    def test_wait_url_contains(self):
        url = self.get_page_url("index.html#section1")
        self.driver.get(url)
        self.wait.until(EC.url_contains("#section1"))
        assert "#section1" in self.driver.current_url

    def test_wait_url_is(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        target_url = self.driver.current_url
        self.wait.until(EC.url_to_be(target_url))

    def test_wait_until_immediate(self):
        result = self._wait_until(lambda: "immediate", timeout=5)
        assert result == "immediate"

    def test_wait_until_delayed(self):
        counter = [0]

        def delayed_result():
            counter[0] += 1
            if counter[0] >= 3:
                return "done"
            return None

        result = self._wait_until(delayed_result, timeout=5, wait_time=0.1)
        assert result == "done"
        assert counter[0] >= 3

    def test_wait_until_timeout(self):
        result = self._wait_until(lambda: None, timeout=2, wait_time=0.2)
        assert result is None

    def _wait_until(self, func, timeout=120, wait_time=0.2):
        import time
        elapsed = 0.0
        result = None
        while elapsed < timeout and result is None:
            try:
                if func is not None:
                    result = func()
            except Exception:
                pass
            time.sleep(wait_time)
            elapsed += wait_time
        return result


from selenium.webdriver.common.by import By