from .test_base import SeleniumTestBase


class TestSeleniumPage(SeleniumTestBase):

    def test_get_new_url(self):
        url1 = self.get_page_url("index.html")
        url2 = self.get_page_url("form.html")
        self.selenium.get(url1)
        assert "index.html" in self.selenium.current_url
        self.selenium.get(url2)
        assert "form.html" in self.selenium.current_url

    def test_get_same_url_reload(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        self.selenium.driver.execute_script("document.getElementById('title').textContent = 'Modified'")
        title = self.selenium.get_by_id("title")
        assert title.text == "Modified"
        self.selenium.get(url)
        title = self.selenium.get_by_id("title")
        assert "Selenium Test Page" in title.text

    def test_reload(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        self.selenium.driver.execute_script("document.getElementById('title').textContent = 'Changed'")
        self.selenium.reload()
        title = self.selenium.get_by_id("title")
        assert "Selenium Test Page" in title.text

    def test_wait_url_contains(self):
        url = self.get_page_url("index.html#section1")
        self.selenium.get(url)
        self.selenium.wait_url_contains("#section1")
        assert "#section1" in self.selenium.current_url

    def test_wait_url_is(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        target_url = self.selenium.current_url
        self.selenium.wait_url_is(target_url)

    def test_wait_until_immediate(self):
        result = self.selenium.wait_until(lambda: "immediate", timeout=5)
        assert result == "immediate"

    def test_wait_until_delayed(self):
        counter = [0]

        def delayed_result():
            counter[0] += 1
            if counter[0] >= 3:
                return "done"
            return None

        result = self.selenium.wait_until(delayed_result, timeout=5, wait_time=0.1)
        assert result == "done"
        assert counter[0] >= 3

    def test_wait_until_timeout(self):
        result = self.selenium.wait_until(lambda: None, timeout=2, wait_time=0.2)
        assert result is None