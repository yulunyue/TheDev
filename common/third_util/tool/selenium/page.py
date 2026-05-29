from typing import Optional, List
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SeleniumPage:
    """页面导航和窗口管理操作"""

    def __init__(self, driver, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait

    def get(self, url: str) -> "SeleniumPage":
        """导航到指定 URL，如果相同则刷新"""
        if self.driver.current_url == url:
            self.reload()
        else:
            self.driver.get(url)
        return self

    def reload(self) -> "SeleniumPage":
        """刷新当前页面"""
        self.driver.refresh()
        return self

    def wait_url_contains(self, key: str) -> None:
        """等待 URL 包含指定字符串"""
        self.wait.until(EC.url_contains(key))

    def wait_url_is(self, url: str, timeout: Optional[int] = None) -> None:
        """等待 URL 等于指定值"""
        self.wait_todo(EC.url_to_be(url), timeout=timeout)

    def wait_todo(self, condition, timeout: Optional[int] = None) -> None:
        """等待条件满足"""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        wait.until(condition)

    def wait_for_window(self) -> Optional[str]:
        """
        等待新窗口打开。

        Returns:
            新窗口的 handle，如果没有新窗口返回 None
        """
        handles_before = self.driver.window_handles

        def window_opened(driver):
            handles_after = self.driver.window_handles
            return list(set(handles_after) - set(handles_before))

        self.wait.until(window_opened)
        handles_after = self.driver.window_handles
        new_handles = list(set(handles_after) - set(handles_before))
        return new_handles[0] if new_handles else None

    def switch_to_window(self, idx: int = -1) -> Optional[str]:
        """
        切换到指定索引的窗口。

        Args:
            idx: 窗口索引，-1 表示最后一个窗口

        Returns:
            切换后的窗口 handle，索引无效返回 None
        """
        handles = self.driver.window_handles
        if idx == -1:
            idx = len(handles) - 1
        if 0 <= idx < len(handles):
            self.driver.switch_to.window(handles[idx])
            return handles[idx]
        return None

    def close_current_window(self) -> None:
        """关闭当前窗口"""
        self.driver.close()

    def get_window_handles(self) -> List[str]:
        """获取所有窗口 handle 列表"""
        return self.driver.window_handles