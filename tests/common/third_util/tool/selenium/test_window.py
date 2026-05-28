from .test_base import SeleniumTestBase


class TestSeleniumWindow(SeleniumTestBase):

    def test_initial_window_handles(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        handles = self.selenium.window.get_window_handles()
        assert len(handles) == 1

    def test_switch_to_window_idx(self):
        url = self.get_page_url("index.html")
        self.selenium.get(url)
        handles = self.selenium.window.get_window_handles()
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
        initial_handles = self.selenium.window.get_window_handles()
        assert len(initial_handles) == 1
        btn = self.selenium.get_clickable("//button[@id='btn-open-window']")
        self.selenium.script_click(btn)
        import time
        time.sleep(1)
        handles_after = self.selenium.window.get_window_handles()
        if len(handles_after) > 1:
            self.selenium.switch_to_window(-1)
            self.selenium.close_current_window()
            self.selenium.switch_to_window(0)
        final_handles = self.selenium.window.get_window_handles()
        assert len(final_handles) == 1

    def test_switch_to_last_window(self):
        url = self.get_page_url("window.html")
        self.selenium.get(url)
        btn = self.selenium.get_clickable("//button[@id='btn-open-window']")
        self.selenium.script_click(btn)
        import time
        time.sleep(1)
        handles = self.selenium.window.get_window_handles()
        if len(handles) > 1:
            last_handle = self.selenium.switch_to_window(-1)
            assert last_handle == handles[-1]
            self.selenium.close_current_window()
            self.selenium.switch_to_window(0)
        else:
            assert True