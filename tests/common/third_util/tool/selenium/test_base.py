import os
import socket
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from common.third_util.tool.selenium import SeleniumUtil


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
    """Selenium 测试基类，使用 SeleniumUtil 封装类"""

    selenium: SeleniumUtil = None
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
        cls.selenium = SeleniumUtil(mode="headless", default_timeout=10).load()

    @classmethod
    def teardown_class(cls):
        if cls.selenium and cls.selenium.driver:
            try:
                cls.selenium.quit()
            except Exception:
                pass
            cls.selenium = None
        cls.http_server.stop()