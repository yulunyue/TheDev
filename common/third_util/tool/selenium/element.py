from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.util.export import List, logger


class SeleniumElement:
    def __init__(self, driver, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait

    def get_by_id(self, key) -> WebElement:
        return self.wait.until(EC.presence_of_element_located((By.ID, key)))

    def get_by_xpath(self, key) -> WebElement:
        return self.wait.until(EC.presence_of_element_located((By.XPATH, key)))

    def get_by_tag(self, key) -> WebElement:
        return self.wait.until(EC.presence_of_element_located((By.TAG_NAME, key)))

    def get_clickable(self, key) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, key)))

    def get_elements_by_xpath(self, key) -> List[WebElement]:
        self.wait.until(EC.presence_of_element_located((By.XPATH, key)))
        return self.find_by_xpath(key)

    def find_by_xpath(self, xpath) -> List[WebElement]:
        return self.driver.find_elements(By.XPATH, xpath)

    def find_by_tag(self, name, **kw) -> List[WebElement]:
        ret = self.driver.find_elements(By.TAG_NAME, name)
        if not kw:
            return ret
        return self.find_by_text(ret, **kw)

    def find_by_text(self, eles: List[WebElement], text=None) -> List[WebElement]:
        ret = []

        def check(e: WebElement):
            if text is not None and text in e.text:
                ret.append(e)

        for e in eles:
            self.dfs(e, check)
        return ret

    def get_children(self, e: WebElement) -> List[WebElement]:
        try:
            return e.find_elements(By.XPATH, ".//*")
        except Exception as ex:
            logger.debug(f"获取子元素失败: {ex}")
            return []

    def dfs(self, e: WebElement, call, parents=None):
        if parents is None:
            parents = [e]
        for v in self.get_children(e):
            call(v, paths=parents + [v])
            self.dfs(v, parents + [v])