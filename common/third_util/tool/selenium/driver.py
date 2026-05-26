from typing import Union, Optional, Dict
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from common.util.export import File, logger, time
from common.tool.export import System, ProcessLock
from .config import SeleniumConfig, USER_DATA_DIR


class SeleniumDriver:
    """
    Selenium Chrome WebDriver 封装。

    模式说明：
    - int: 调试模式，连接已有 Chrome 实例的端口
    - "headless": 无头模式，独立启动 Chrome
    - 其他字符串: 独立实例模式，使用独立的 user-data 目录
    """

    def __init__(
        self,
        mode: Union[int, str] = 9527,
        default_timeout: int = 6,
        bypass_proxy: bool = False,
    ):
        self.mode = mode
        self.default_timeout = default_timeout
        self._bypass_proxy = bypass_proxy
        self.driver: Optional[WebDriver] = None
        self.wait: Optional[WebDriverWait] = None
        self.options: Optional[Options] = None

    def load(self) -> "SeleniumDriver":
        chrome_exe_file, chrome_driver_file = SeleniumConfig.ensure_chrome()
        user_data_dir = File(USER_DATA_DIR).make_dir_if_not_exist(True)

        if isinstance(self.mode, int):
            self._setup_debug_mode(chrome_exe_file, user_data_dir)

        if self.driver is None:
            self._create_driver(chrome_exe_file, chrome_driver_file, user_data_dir)

        return self

    def _setup_debug_mode(self, chrome_exe_file: File, user_data_dir: File) -> None:
        lock = ProcessLock(f"chrome_{self.mode}")
        if lock.is_running():
            return

        pid = System.get_pid_by_port(self.mode)
        if pid:
            lock.set_pid(pid)
            return

        lock.start_process(
            chrome_exe_file.get_abs_path(),
            f"--remote-debugging-port={self.mode}",
            f"--user-data-dir={user_data_dir.get_abs_path()}",
            "--disable-gpu",
            "--no-first-run",
            "--disable-extensions",
        )
        time.sleep(2)

    def _create_driver(
        self, chrome_exe_file: File, chrome_driver_file: File, user_data_dir: File
    ) -> None:
        self.options = Options()
        service = Service(
            chrome_driver_file.get_abs_path(),
            service_args=["--verbose", "--log-path=data/log/chromedriver.log"],
        )

        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--no-first-run")
        self.options.add_argument("--ignore-certificate-errors")

        if self._bypass_proxy:
            self.options.add_argument("--proxy-server='direct://'")
            self.options.add_argument("--proxy-bypass-list=*")

        if isinstance(self.mode, int):
            self.options.debugger_address = f"127.0.0.1:{self.mode}"
            self.options.add_argument("--start-maximized")
        else:
            if self.mode == "headless":
                self.options.add_argument("--headless")
            self.options.binary_location = chrome_exe_file.get_abs_path()
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--window-size=1920,1080")
            user_data = (
                chrome_driver_file.parent()
                .child(f"dev_user_data_{self.mode}")
                .make_dir_if_not_exist(True)
            )
            self.options.add_argument(f"--user-data-dir={user_data.get_abs_path()}")

        self.driver = webdriver.Chrome(options=self.options, service=service)
        self.wait = WebDriverWait(self.driver, self.default_timeout)

    def quit(self) -> None:
        """销毁 WebDriver 实例"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.wait = None
            self.options = None

    def get_cookies(
        self, name: Optional[str] = None
    ) -> Union[Dict[str, str], str, None]:
        """
        获取 Cookie。

        Args:
            name: 指定 Cookie 名称时返回对应值，否则返回全部 Cookie 字典

        Returns:
            指定名称时返回字符串，否则返回字典
        """
        cookies = self.driver.get_cookies()
        ret = {c["name"]: c["value"] for c in cookies}
        if name is not None:
            return ret.get(name)
        return ret
