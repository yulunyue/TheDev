from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from common.util.export import File, logger, time
from common.tool.export import System, ProcessLock
from .config import SeleniumConfig, USER_DATA_DIR


class SeleniumDriver:
    driver: WebDriver = None
    wait: WebDriverWait = None
    options: Options = None

    def __init__(self, dev_port=9527, default_timeout=6, bypass_proxy=False, auto_start=True):
        self.dev_port = dev_port
        self.default_timeout = default_timeout
        self._bypass_proxy = bypass_proxy
        self.auto_start = auto_start

    def load(self):
        chrome_exe_file, chrome_driver_file = SeleniumConfig.ensure_chrome()
        user_data_dir = File(USER_DATA_DIR).make_dir_if_not_exist(True)

        if isinstance(self.dev_port, int):
            lock = ProcessLock(f"chrome_{self.dev_port}")
            if not lock.is_running():
                pid = System.get_pid_by_port(self.dev_port)
                if pid:
                    lock.set_pid(pid)
                elif self.auto_start:
                    lock.start_process(
                        chrome_exe_file.get_abs_path(),
                        f"--remote-debugging-port={self.dev_port}",
                        f"--user-data-dir={user_data_dir.get_abs_path()}",
                        "--disable-gpu",
                        "--no-first-run",
                        "--disable-extensions",
                    )
                    time.sleep(2)
                else:
                    raise Exception(
                        " ".join([
                            chrome_exe_file.get_abs_path(),
                            f"--remote-debugging-port={self.dev_port}",
                            f'--user-data-dir="{user_data_dir.get_abs_path()}"',
                        ])
                    )

        if self.driver is None:
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

            if isinstance(self.dev_port, int):
                self.options.debugger_address = f"127.0.0.1:{self.dev_port}"
                self.options.add_argument("--start-maximized")
            else:
                if self.dev_port == "headless":
                    self.options.add_argument("--headless")
                self.options.binary_location = chrome_exe_file.get_abs_path()
                self.options.add_argument("--no-sandbox")
                self.options.add_argument("--window-size=1920,1080")
                user_data = chrome_driver_file.parent().child(f"dev_user_data_{self.dev_port}").make_dir_if_not_exist(True)
                self.options.add_argument(f"--user-data-dir={user_data.get_abs_path()}")

            self.driver = webdriver.Chrome(options=self.options, service=service)
            self.wait = WebDriverWait(self.driver, self.default_timeout)

        return self

    def quit(self):
        if self.driver:
            self.driver.quit()
            self.driver = None