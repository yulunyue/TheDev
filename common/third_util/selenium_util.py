from selenium import webdriver
from common.tool.export import OsUtil, GC, System
from common.service.export import Api
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

    def e_format_node(self, element: WebElement, text_max_size=20):
        ret = [""]
        element_id = element.get_attribute("id")
        tag_name = element.tag_name
        # 获取其他有用的属性
        class_attr = element.get_attribute("class") or ""
        name_attr = element.get_attribute("name") or ""
        url = element.get_attribute("url") or ""
        title = element.get_attribute("title") or ""
        disabled = element.get_attribute("disabled")
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
        ret.append(
            "; ".join(
                [
                    f"标签: <{tag_name}>",
                    f"ID: [{element_id}]",
                    f"title: [{title}]",
                    f"disabled: [{disabled}]",
                    f"type: [{element.get_attribute('type')}]",
                ]
            )
        )
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

    def e_format(self, element: WebElement, text_max_size=20):
        if isinstance(element, list):
            rets = []
            for e in element:
                rets.append(self.e_format_node(e, text_max_size))
            return "\n".join(rets)
        return self.e_format_node(element, text_max_size)

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

    def load(self, dev_port=9255):
        user_data_dir = File("data/chrome").make_dir_if_not_exist(True)

        if dev_port:
            chrome_exe = File(GC.chrome_bin_path.get_value())
            chrome_driver = File(GC.chrome_driver_path.get_value())
            if not chrome_exe.exists():
                Api().download(GC.chrome_bin_uri.get_value()).unzip(chrome_exe.path)
            if not chrome_driver.exists():
                Api().download(GC.chrome_driver_uri.get_value()).unzip(
                    chrome_driver.path
                )
            if not chrome_exe.exists() or not chrome_driver.exists():
                raise Exception(
                    f"Chrome or ChromeDriver 下载失败,{chrome_exe.path} {chrome_driver.path}"
                )
            os_util = OsUtil(chrome_exe.child("chrome-win64/chrome.exe").get_abs_path())
            info = System.check_port(dev_port)
            if not info:
                raise Exception(
                    " ".join(
                        [
                            os_util.fun_name,
                            f"--remote-debugging-port={dev_port}",
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
            self.options.add_argument("--auto-open-devtools-for-tabs")
            self.options.add_argument("--disable-extensions")  # 禁用扩展
            self.options.add_argument("--no-first-run")  # 跳过首次运行提示
            # 启用 CDP
            # self.options.add_experimental_option(
            #     "excludeSwitches", ["enable-automation"]
            # )
            # self.options.add_experimental_option("useAutomationExtension", False)
            # 设置性能日志
            # caps = self.options.to_capabilities()
            # caps["goog:loggingPrefs"] = {"performance": "ALL"}

            if dev_port:
                self.options.debugger_address = f"127.0.0.1:{dev_port}"
            else:
                self.options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=self.options, service=service)
            self.wait = WebDriverWait(self.driver, 15)
            # self.driver.set_page_load_timeout(10)

        return self

    def intercept_window_open(self):
        """拦截 window.open 调用"""

        # 重写 window.open 方法
        script = """
        // 保存原始的 window.open
        window._originalOpen = window.open;
        
        // 重写 window.open
        window.open = function(url, windowName, windowFeatures) {
            console.log('[Interceptor] window.open called:', url, windowName, windowFeatures);
            
            // 触发自定义事件
            var event = new CustomEvent('windowOpenIntercepted', {
                detail: {
                    url: url,
                    windowName: windowName,
                    windowFeatures: windowFeatures,
                    timestamp: Date.now()
                }
            });
            window.dispatchEvent(event);
            
            // 返回 null 或模拟的窗口对象
            return {
                closed: false,
                close: function() {
                    console.log('[Interceptor] Mock window closed');
                    this.closed = true;
                },
                location: {
                    href: url
                }
            };
        };
        
        // 监听拦截事件
        window.addEventListener('windowOpenIntercepted', function(e) {
            console.log('Window open intercepted:', e.detail);
        });
        
        console.log('Window.open interception activated');
        """

        self.driver.execute_script(script)

    @property
    def current_url(self):
        return self.driver.current_url

    def get(self, url):

        self.load()
        if self.driver.current_url == url:
            return url
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
        return self.current_url

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

            return "todo"
        except Exception as e:
            return str(e)
