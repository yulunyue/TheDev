import os
import shutil
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop

PORT_BASE = 50040
TEST_DIR = "data/tmp/test_api_io"


class TestHandler(RequestHandler):
    """测试专用 HTTP Handler"""

    def get(self, path):
        if path == "test.txt":
            self.write(b"Hello World")
        elif path == "large.bin":
            size = 5 * 1024 * 1024
            self.set_header("Content-Length", str(size))
            self.write(os.urandom(size))
        elif path == "error":
            self.set_status(404)
            self.write(b"Not Found")
        elif path == "json":
            self.write(b'{"key": "value"}')
        elif path == "query":
            self.write(b"query test")
        else:
            self.set_status(404)

    def post(self, path):
        if path == "json":
            import json

            body = self.request.body
            if body:
                data = json.loads(body)
                self.write(json.dumps({"received": data}))
            else:
                self.write(b'{"received": null}')
        else:
            self.set_status(404)


def setup_http_server():
    """启动 HTTP 测试服务"""
    app = Application([(r"/test/(.*)", TestHandler)])
    app.listen(PORT_BASE, "127.0.0.1")
    return app


def setup_test_dir():
    """创建测试目录"""
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR, exist_ok=True)


def teardown_test_dir():
    """清理测试目录"""
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)


def clear_tmp_download_files():
    """清理 download 临时文件"""
    tmp_dir = "data/tmp"
    if os.path.exists(tmp_dir):
        for f in os.listdir(tmp_dir):
            if f.startswith("download_"):
                try:
                    os.remove(os.path.join(tmp_dir, f))
                except Exception:
                    pass


def clear_download_dir():
    """清理 download 目录"""
    download_dir = "data/download"
    if os.path.exists(download_dir):
        for f in os.listdir(download_dir):
            try:
                os.remove(os.path.join(download_dir, f))
            except Exception:
                pass