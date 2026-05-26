from selenium.webdriver.support.ui import WebDriverWait


class SeleniumWindow:
    def __init__(self, driver, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait

    def wait_for_window(self) -> str:
        handles_before = self.driver.window_handles

        def window_opened(driver):
            handles_after = self.driver.window_handles
            return list(set(handles_after) - set(handles_before))

        self.wait.until(window_opened)
        handles_after = self.driver.window_handles
        new_handles = list(set(handles_after) - set(handles_before))
        return new_handles[0] if new_handles else None

    def switch_to_window(self, idx=-1) -> str:
        handles = self.driver.window_handles
        if idx == -1:
            idx = len(handles) - 1
        if 0 <= idx < len(handles):
            self.driver.switch_to.window(handles[idx])
            return handles[idx]
        return None

    def close_current_window(self):
        self.driver.close()