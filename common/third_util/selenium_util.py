from selenium import webdriver
from common.tool.export import OsUtil, GC
from selenium.webdriver.chrome.options import Options
from common.util.export import File, logger
from selenium.webdriver.chrome.service import Service
import tempfile


class SeleniumUtil:
    driver: webdriver.Chrome = None

    def __init__(self, url):
        self.root_url = url

    def load(self, dev_port=9222):
        user_data_dir = File("data/chrome").make_dir_if_not_exist(True)
        # user_data_dir = tempfile.mkdtemp()
        os_util = OsUtil(GC.chrome_bin_path.get_value())
        if dev_port:
            info = os_util.check_port(dev_port)
            if not info:
                os_util.run(
                    f"--remote-debugging-port={dev_port}",
                    f'--user-data-dir="{user_data_dir.get_abs_path()}"',
                )
                info1 = os_util.check_port(dev_port)
                if not info1:
                    return
            else:
                logger.info(info)
        if self.driver is None:
            self.options = Options()
            # service = Service(
            #     log_path="data/log/chromedriver.log", service_args=["--verbose"]
            # )
            if dev_port:
                self.options.debugger_address = f"127.0.0.1:{dev_port}"
                # self.options.add_experimental_option(
                #     "excludeSwitches", ["enable-automation"]
                # )
            self.driver = webdriver.Chrome(options=self.options)  # , service=service)
            # self.driver.set_page_load_timeout(10)

        return self

    def run(self):
        self.load()
        self.driver.get(self.root_url)
