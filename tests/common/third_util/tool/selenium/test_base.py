import os
import socket
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

CHROME_BIN_PATH = "D:/thedev/data/chrome_bin/chrome-win64/chrome.exe"
CHROMEDRIVER_PATH = "D:/thedev/data/chrome_driver/chromedriver-win64/chromedriver.exe"


class TestHTTPServer:
    """本地 HTTP Server 用于测试"""

    _server = None
    _thread = None
    _port = None

    @classmethod
    def start(cls, directory: str, port: int = 0):
        if port == 0:
            port = cls._find_free_port()
        cls._port = port

        class Handler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=directory, **kwargs)

        cls._server = HTTPServer(("127.0.0.1", port), Handler)
        cls._thread = threading.Thread(target=cls._server.serve_forever, daemon=True)
        cls._thread.start()
        time.sleep(0.3)
        return port

    @classmethod
    def stop(cls):
        if cls._server:
            cls._server.shutdown()
            cls._server = None
            cls._thread = None

    @classmethod
    def get_url(cls, page_name: str) -> str:
        return f"http://127.0.0.1:{cls._port}/{page_name}"

    @staticmethod
    def _find_free_port() -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            return s.getsockname()[1]


class SeleniumTestBase:
    """Selenium 测试基类"""

    driver = None
    wait = None
    http_server = TestHTTPServer
    TEST_PAGE_DIR = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "..", "..", "data", "tmp", "selenium_test"
        )
    )

    @classmethod
    def get_page_url(cls, page_name: str) -> str:
        return cls.http_server.get_url(page_name)

    @classmethod
    def setup_class(cls):
        cls.http_server.start(cls.TEST_PAGE_DIR)
        cls._setup_driver()

    @classmethod
    def _setup_driver(cls):
        cls.options = Options()
        cls.options.binary_location = CHROME_BIN_PATH
        cls.options.add_argument("--headless=new")
        cls.options.add_argument("--no-sandbox")
        cls.options.add_argument("--disable-dev-shm-usage")
        cls.options.add_argument("--disable-gpu")
        cls.options.add_argument("--disable-software-rasterizer")
        cls.options.add_argument("--disable-extensions")
        cls.options.add_argument("--disable-popup-blocking")
        cls.options.add_argument("--disable-translate")
        cls.options.add_argument("--disable-sync")
        cls.options.add_argument("--metrics-recording-only")
        cls.options.add_argument("--disable-background-networking")
        cls.options.add_argument("--disable-default-apps")
        cls.options.add_argument("--no-first-run")
        cls.options.add_argument("--window-size=1920,1080")
        cls.options.add_argument("--ignore-certificate-errors")
        cls.options.add_argument("--remote-allow-origins=*")
        cls.options.add_argument("--log-level=3")
        cls.options.page_load_strategy = "normal"
        service = Service(executable_path=CHROMEDRIVER_PATH)
        cls.driver = webdriver.Chrome(service=service, options=cls.options)
        cls.driver.set_page_load_timeout(30)
        cls.wait = WebDriverWait(cls.driver, 10)

    @classmethod
    def teardown_class(cls):
        if cls.driver:
            try:
                cls.driver.quit()
            except Exception:
                pass
            cls.driver = None
            cls.wait = None
        cls.http_server.stop()