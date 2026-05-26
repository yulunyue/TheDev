from common.util.export import logger, time, url_parse
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SeleniumPage:
    def __init__(self, driver, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait
        self.wait_result = None
        self.last_url = None
        self.request_offset_size = 0

    def get(self, url):
        if self.driver.current_url == url:
            self.reload()
        else:
            self.driver.get(url)
        return self

    def reload(self):
        self.driver.refresh()
        return self

    def wait_url_contains(self, key):
        self.wait.until(EC.url_contains(key))

    def wait_url_is(self, url, timeout=None):
        self.wait_todo(EC.url_to_be(url), timeout=timeout)

    def wait_todo(self, f, timeout=None):
        if timeout is None:
            wait = self.wait
        else:
            wait = WebDriverWait(self.driver, timeout)
        wait.until(f)

    def wait_until(self, func=None, timeout=120, wait_time=0.2):
        self.wait_result = None
        self.last_url = None
        self.request_offset_size = 0
        try:
            while timeout > 0 and self.wait_result is None:
                new_url, args, kw = url_parse(self.driver.current_url)
                if self.last_url != new_url:
                    pass
                if func is not None:
                    self.wait_result = func()
                self.last_url = new_url
                timeout -= wait_time
                time.sleep(wait_time)
        except Exception as e:
            logger.exception(e)
        finally:
            self.driver.quit()
        return self.wait_result