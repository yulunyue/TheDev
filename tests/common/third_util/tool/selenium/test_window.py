from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .test_base import SeleniumTestBase


class TestSeleniumWindow(SeleniumTestBase):

    def test_initial_window_handles(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        handles = self.driver.window_handles
        assert len(handles) == 1

    def test_switch_to_window_idx(self):
        url = self.get_page_url("index.html")
        self.driver.get(url)
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[0])
        assert self.driver.current_window_handle == handles[0]

    def test_open_and_close_window(self):
        url = self.get_page_url("window.html")
        self.driver.get(url)
        initial_handles = self.driver.window_handles
        assert len(initial_handles) == 1
        btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='btn-open-window']")))
        btn.click()

        def window_opened(driver):
            handles_after = driver.window_handles
            new_handles = list(set(handles_after) - set(initial_handles))
            return new_handles[0] if new_handles else False

        new_handle = self.wait.until(window_opened)
        handles_after = self.driver.window_handles
        assert len(handles_after) == 2
        self.driver.switch_to.window(handles_after[-1])
        self.driver.close()
        self.driver.switch_to.window(handles_after[0])
        final_handles = self.driver.window_handles
        assert len(final_handles) == 1

    def test_switch_to_last_window(self):
        url = self.get_page_url("window.html")
        self.driver.get(url)
        btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='btn-open-window']")))
        btn.click()

        def window_opened(driver):
            handles = driver.window_handles
            return len(handles) > 1

        self.wait.until(window_opened)
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[-1])
        assert self.driver.current_window_handle == handles[-1]
        self.driver.close()
        self.driver.switch_to.window(handles[0])