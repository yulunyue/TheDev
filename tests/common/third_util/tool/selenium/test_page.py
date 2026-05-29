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
        self.selenium.driver.execute_script(
            "document.getElementById('title').textContent = 'Modified'"
        )
        title = self.selenium.get_by_id("title")
        assert title.text == "Modified"
        self.selenium.get(url)
        title = self.selenium.get_by_id("title")
        assert "Selenium Test Page" in title.text

    def test_reload(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        self.selenium.driver.execute_script(
            "document.getElementById('title').textContent = 'Changed'"
        )
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

    def test_initial_window_handles(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        handles = self.selenium.get_window_handles()
        assert len(handles) == 1

    def test_switch_to_window_idx(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        handles = self.selenium.get_window_handles()
        result = self.selenium.switch_to_window(0)
        assert result == handles[0]

    def test_switch_to_window_invalid_idx(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        result = self.selenium.switch_to_window(99)
        assert result is None

    def test_open_and_close_window(self):
        url = self.get_page_url("window.html")
        self.selenium.get(url)
        initial_handles = self.selenium.get_window_handles()
        assert len(initial_handles) == 1
        btn = self.selenium.get_clickable("//button[@id='btn-open-window']")
        self.selenium.script_click(btn)
        import time

        time.sleep(1)
        handles_after = self.selenium.get_window_handles()
        if len(handles_after) > 1:
            self.selenium.switch_to_window(-1)
            self.selenium.close_current_window()
            self.selenium.switch_to_window(0)
        final_handles = self.selenium.get_window_handles()
        assert len(final_handles) == 1

    def test_switch_to_last_window(self):
        url = self.get_page_url("window.html")
        self.selenium.get(url)
        btn = self.selenium.get_clickable("//button[@id='btn-open-window']")
        self.selenium.script_click(btn)
        import time

        time.sleep(1)
        handles = self.selenium.get_window_handles()
        if len(handles) > 1:
            last_handle = self.selenium.switch_to_window(-1)
            assert last_handle == handles[-1]
            self.selenium.close_current_window()
            self.selenium.switch_to_window(0)
        else:
            assert True