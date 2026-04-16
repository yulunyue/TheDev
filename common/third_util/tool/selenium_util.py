# from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from seleniumwire import webdriver
from seleniumwire.request import Request, Response
from common.tool.export import OsUtil, GC, System

from selenium.webdriver.chrome.options import Options

Chrome = webdriver.Chrome
from common.util.export import File, logger, time, List, url_to_json, url_parse
from selenium.webdriver.chrome.service import Service


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from .selenium_script import wart_until_doc_ready


class SeleniumUtil:
    driver: WebDriver = None

    def __init__(self, dev_port=9527, default_time_out=6):
        self.dev_port = dev_port
        self.default_time_out = default_time_out

    @property
    def logger(self):
        return logger

    def print_info(self):
        for e in self.find_elements_by_xpath("//*[text()!='']"):
            try:
                er = self.e_format(e)
            except Exception as e2:
                er = f"{e}:{e2}"
            self.logger.debug(er)

    def get_element_by_id(self, key):
        return self.wait.until(EC.presence_of_element_located((By.ID, key)))

    def get_element_by_xpath(self, key) -> WebElement:
        return self.wait.until(EC.presence_of_element_located((By.XPATH, key)))

    def get_elements_by_xpath(self, key) -> List[WebElement]:
        self.wait.until(EC.presence_of_element_located((By.XPATH, key)))
        return self.find_elements_by_xpath(key)

    def get_clickable_by_xpath(self, key):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, key)))

    def get_element_by_tag(self, key):
        return self.wait.until(EC.presence_of_element_located((By.TAG_NAME, key)))

    def find_elements_by_xpath(self, xpath):
        return self.driver.find_elements(By.XPATH, xpath)

    def find_elements_by_tag(self, name, **kw):
        ret = self.driver.find_elements(By.TAG_NAME, name)
        if not kw:
            return ret
        return self.find_elements_by_text(ret, **kw)

    def find_elements_by_text(self, eles: List[WebElement], text=None):
        ret = []

        def util(e: WebElement, **kw):
            if text is not None and text in e.text:
                ret.append(e)

        for e in eles:
            self.dfs(e, util)
        return ret

    def get_children(self, e: WebElement):
        try:
            return e.find_elements(".//*")
        except Exception as e2:
            logger.debug(f"获取子元素{e2}失败: {self.e_format(e)}")
            return []

    def dfs(self, e: WebElement, call, parents=None):
        if parents is None:
            parents = [e]
        for v in self.get_children(e):
            call(v, paths=parents + [v])
            self.dfs(v, parents + [v])

    def print(self, e: WebElement):
        self.dfs(e, call=lambda ele, paths: logger.debug(self.e_format(ele)))

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

    def request_interceptor(self, request: Request):
        logger.map(uri=request.url, method=request.method, headers=request.headers)

    def response_interceptor(self, request: Request, response: Response):
        logger.map(uri=request.url, method=request.method, headers=request.headers)

    def load(self):
        user_data_dir = File("data/chrome").make_dir_if_not_exist(True)
        chrome_exe = File(GC.chrome_bin_path.get_value())
        chrome_driver = File(GC.chrome_driver_path.get_value())
        from common.third_util.io.api import Api

        if not chrome_exe.exists():
            Api().download(GC.chrome_bin_uri.get_value()).unzip(chrome_exe.path)
        if not chrome_driver.exists():
            Api().download(GC.chrome_driver_uri.get_value()).unzip(chrome_driver.path)
        if not chrome_exe.exists() or not chrome_driver.exists():
            raise Exception(
                f"Chrome or ChromeDriver 下载失败,{chrome_exe.path} {chrome_driver.path}"
            )
        chrome_exe_file = chrome_exe.child("chrome-win64/chrome.exe")
        if isinstance(self.dev_port, int):
            info = System.get_pid_by_port(self.dev_port)
            if not info:
                raise Exception(
                    " ".join(
                        [
                            chrome_exe_file.get_abs_path(),
                            f"--remote-debugging-port={self.dev_port}",
                            f'--user-data-dir="{user_data_dir.get_abs_path()}"',
                        ]
                    )
                )

        if self.driver is None:
            self.options = Options()
            service = Service(
                chrome_driver.child(
                    "chromedriver-win64/chromedriver.exe"
                ).get_abs_path(),
                service_args=["--verbose", "--log-path=data/log/chromedriver.log"],
            )

            # self.options.add_argument("--auto-open-devtools-for-tabs")
            self.options.add_argument("--disable-extensions")  # 禁用扩展
            self.options.add_argument("--no-first-run")  # 跳过首次运行提示
            self.options.add_argument("--ignore-certificate-errors")
            if isinstance(self.dev_port, int):
                self.options.debugger_address = f"127.0.0.1:{self.dev_port}"
                self.options.add_argument("--start-maximized")
            else:
                if self.dev_port != "dev":
                    self.options.add_argument("--headless")
                self.options.binary_location = chrome_exe_file.get_abs_path()
                self.options.add_argument("--no-sandbox")
                self.options.add_argument("--window-size=1920,1080")
                self.options.add_argument(
                    f"--user-data-dir={chrome_driver.child('dev_user_data12').make_dir_if_not_exist(True).get_abs_path()}"
                )
            self.driver = Chrome(
                options=self.options,
                service=service,
                # seleniumwire_options=dict(
                #     request_interceptor=self.request_interceptor,
                #     response_interceptor=self.response_interceptor,
                # ),
            )
            self.wait = WebDriverWait(self.driver, self.default_time_out)
            # self.driver.set_page_load_timeout(10)

        return self

    def url_change(self, f: str, t: str):
        pass

    def get(self, url):
        self.load()
        if self.driver.current_url == url:
            self.reload()
        else:
            self.driver.get(url)
        return self

    def wait_until(self, func=None, time_out=120, wait_time=0.2):
        self.wait_result = None
        self.last_url = None

        self.request_offset_size = 0
        try:
            while time_out > 0 and self.wait_result is None:
                new_url, args, kw = url_parse(self.driver.current_url)
                if self.last_url != new_url:
                    # wart_until_doc_ready(self.wait)
                    self.url_change(self.last_url, new_url)
                self.handel_new_requests()
                if func is not None:
                    self.wait_result = func()
                self.last_url = new_url
                time_out -= wait_time
                time.sleep(wait_time)
        except Exception as e:
            logger.exception(e)
        finally:
            self.driver.quit()
        return self.wait_result

    def handel_new_requests(self) -> List[Request]:
        requests: List[Request] = self.driver.requests
        while self.request_offset_size < len(requests):
            self.request_interceptor(requests[self.request_offset_size])
            self.request_offset_size += 1

    def wait_for_window(self):
        """等待新窗口打开"""
        handles_before = self.driver.window_handles

        def window_opened(driver):
            handles_after = self.driver.window_handles
            return list(set(handles_after) - set(handles_before))

        self.wait.until(window_opened)

        # 返回新窗口句柄
        handles_after = self.driver.window_handles
        new_handles = list(set(handles_after) - set(handles_before))
        return new_handles[0] if new_handles else None

    def switch_to_window(self, idx=-1):
        """切换到某一个窗口"""
        handles = self.driver.window_handles
        if idx == -1:
            idx = len(handles) - 1
        if 0 <= idx <= len(handles):
            self.driver.switch_to.window(handles[idx])
            return handles[idx]
        return False

    def close_current_window(self):
        """关闭当前窗口"""
        self.driver.close()

    def script_scroll(self, ele):
        self.driver.execute_script("arguments[0].scrollIntoView();", ele)

    def script_click(self, ele):
        self.driver.execute_script("arguments[0].click();", ele)

    def reload(self):
        self.driver.refresh()
        return self

    def get_cookies(self, name=None):
        cookies = self.driver.get_cookies()
        ret = dict()
        for c in cookies:
            if name is not None and c["name"] == name:
                return c["value"]
            ret[c["name"]] = c["value"]
        return ret

    def do_cmd(self, method, *args):
        try:
            if method == "go":
                return self.get(*args)
            elif method == "path":
                return self.e_format(self.get_elements_by_xpath(args[0]))
            elif method == "click":
                return self.get_element_by_xpath(args[0]).click()
            elif method == "open":
                self.get_element_by_xpath(args[0]).click()
                self.wait_for_window()
                self.switch_to_window()
                return self.current_url
            elif method == "reload":
                return self.reload()
            elif method == "sendkeys":
                r = self.get_element_by_xpath(args[0])
                r.clear()
                return r.send_keys(args[1])
            elif method == "id":
                return self.e_format(self.get_element_by_id(args[0]))
            elif method == "get_cookies":
                name = None if len(args) == 0 else args[0]
                return self.get_cookies(name=name)
            return "todo"
        except Exception as e:
            return str(e)

    def do_cmds(self, *args):
        for a in args:
            self.do_cmd(a)
