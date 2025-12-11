from selenium import webdriver
from common.tool.export import OsUtil, GC
from selenium.webdriver.chrome.options import Options
from common.util.export import File, logger, time, List
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class SeleniumUtil:
    driver: webdriver.Chrome = None

    @property
    def logger(self):
        return logger

    def get_xpath_from_chrome_devtools(self, element):
        """
        模拟 Chrome DevTools 复制 XPath 的功能
        """
        js_code = """
        function getXPathForElement(element) {
            const idx = (sib, name) => sib 
                ? idx(sib.previousElementSibling, name||sib.localName) + (sib.localName == name)
                : 1;
            const segs = elm => !elm || elm.nodeType !== 1 
                ? ['']
                : elm.id && document.getElementById(elm.id) === elm
                    ? [`//*[@id="${elm.id}"]`]
                    : [...segs(elm.parentNode), `${elm.localName.toLowerCase()}[${idx(elm)}]`];
            return segs(element).join('/');
        }
        return getXPathForElement(arguments[0]);
        """

        return self.driver.execute_script(js_code, element)

    def e_format(self, element: WebElement, text_max_size=100):
        ret = []
        element_id = element.get_attribute("id")
        tag_name = element.tag_name
        # 获取其他有用的属性
        class_attr = element.get_attribute("class") or ""
        name_attr = element.get_attribute("name") or ""
        url = element.get_attribute("url") or ""
        # 获取位置和大小
        location_str = ""
        try:
            location = element.location
            size = element.size
            location_str = f"位置: ({location['x']}, {location['y']}); 大小: {size['width']}x{size['height']}"

        except:
            location_str = ""
        # 获取可见文本（截断）
        try:
            text = element.text.strip()
            if len(text) > text_max_size * 2:
                text = text[:text_max_size] + "..." + text[-text_max_size:]
        except:
            text = ""
        ret.append(f"\n 标签: <{tag_name}>; ID: '{element_id}'")
        ret.append(f"   XPATH:{self.get_xpath_from_chrome_devtools(element)} ")
        if class_attr:
            ret.append(f"   类: {class_attr};")

        if name_attr:
            ret.append(f"   Name: {name_attr}")
        if url:
            ret.append(f"   uri: {url}")
        ret.append(f"   {location_str}")
        if text:
            ret.append(f"   文本: {text}")

        return "\n".join(ret)

    def print_info(self):
        for e in self.find_elements_by_xpath("//*[text()!='']"):
            try:
                er = self.e_format(e)
            except Exception as e2:
                er = f"{e}:{e2}"
            self.logger.debug(er)

    def play(self, fun):
        try:
            fun()
        except Exception as e:
            raise Exception(e)
        finally:
            self.print_info()

    def get_element_by_id(self, key):
        return self.wait.until(EC.presence_of_element_located((By.ID, key)))

    def get_element_by_xpath(self, key):
        return self.wait.until(EC.presence_of_element_located((By.XPATH, key)))

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
        return e.find_elements(".//*")

    def dfs(self, e: WebElement, call, parents=None):
        if parents is None:
            parents = [e]
        for v in self.get_children(e):
            call(v, paths=parents + [v])
            self.dfs(v, parents + [v])

    def wait_url_contains(self, key):
        self.wait.until(EC.url_contains(key))

    def load(self, dev_port=9222):
        user_data_dir = File("data/chrome").make_dir_if_not_exist(True)
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
            service = Service(
                "D:/tool/chromedriver-win64_143/chromedriver-win64/chromedriver.exe",
                service_args=["--verbose", "--log-path=data/log/chromedriver.log"],
            )
            self.options.add_argument("--auto-open-devtools-for-tabs")
            self.options.add_argument("--disable-extensions")  # 禁用扩展
            self.options.add_argument("--no-first-run")  # 跳过首次运行提示
            if dev_port:
                self.options.debugger_address = f"127.0.0.1:{dev_port}"
            else:
                self.options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=self.options, service=service)
            self.wait = WebDriverWait(self.driver, 5)
            # self.driver.set_page_load_timeout(10)

        return self

    def get(self, url):
        self.driver.get(url)
        current_url = self.driver.current_url
        for _ in range(7):
            self.wait.until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            time.sleep(1)
            new_url = self.driver.current_url
            if new_url == current_url:
                break
            current_url = new_url
            logger.info(f"HTTP重定向到: {current_url}")

        return current_url

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
            return True
        return False

    def script_scroll(self, ele):
        self.driver.execute_script("arguments[0].scrollIntoView();", ele)

    def script_click(self, ele):
        self.driver.execute_script("arguments[0].click();", ele)
