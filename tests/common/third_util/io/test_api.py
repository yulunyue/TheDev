import os
import shutil
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from common.third_util.io.api import Api
from common.util.export import File

TEST_DIR = "data/tmp/test_api_io"
PORT = 50041


class TestHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        filename = path.split("/")[-1]
        query = urlparse(self.path).query

        if filename == "test.txt":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", "11")
            self.end_headers()
            self.wfile.write(b"Hello World")
        elif filename == "large.bin":
            size = 1 * 1024 * 1024
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", str(size))
            self.end_headers()
            self.wfile.write(os.urandom(size))
        elif filename == "error":
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not Found")
        elif filename == "query":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", "10")
            self.end_headers()
            self.wfile.write(b"query test")
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        path = urlparse(self.path).path
        filename = path.split("/")[-1]
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b""

        if filename == "json":
            import json

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            if body:
                data = json.loads(body)
                self.wfile.write(json.dumps({"received": data}).encode())
            else:
                self.wfile.write(b'{"received": null}')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


_http_server = None
_http_thread = None


def start_http_server():
    global _http_server, _http_thread
    _http_server = HTTPServer(("127.0.0.1", PORT), TestHTTPHandler)
    _http_thread = threading.Thread(target=_http_server.serve_forever, daemon=True)
    _http_thread.start()
    time.sleep(0.3)


def stop_http_server():
    global _http_server
    if _http_server:
        _http_server.shutdown()
        time.sleep(0.1)


class TestApiDownload:
    @classmethod
    def setup_class(cls):
        if os.path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)
        os.makedirs(TEST_DIR, exist_ok=True)
        start_http_server()
        cls.api = Api("test_api")

    @classmethod
    def teardown_class(cls):
        stop_http_server()
        if os.path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)
        clear_tmp_download_files()
        clear_download_dir()

    def setup_method(self):
        clear_tmp_download_files()
        clear_download_dir()

    def teardown_method(self):
        clear_tmp_download_files()
        clear_download_dir()

    def test_download_success(self):
        url = f"http://127.0.0.1:{PORT}/test/test.txt"
        dst = f"{TEST_DIR}/test.txt"
        result = self.api.download(url, dst=dst)
        assert result.exists()
        assert result.read_data() == b"Hello World"
        self._assert_no_tmp_files()

    def test_download_no_dst_exists(self):
        url = f"http://127.0.0.1:{PORT}/test/test.txt"
        dst = f"{TEST_DIR}/exist.txt"
        File(dst).write_file(b"pre-existing")
        result = self.api.download(url, dst=dst)
        assert result.read_data() == b"pre-existing"

    def test_download_no_http_404(self):
        url = f"http://127.0.0.1:{PORT}/test/error"
        dst = f"{TEST_DIR}/error.txt"
        try:
            self.api.download(url, dst=dst)
        except Exception as e:
            assert "404" in str(e) or "404" in str(e.args)
        finally:
            assert not os.path.exists(dst)
            self._assert_no_tmp_files()

    def test_sequential_download(self):
        base_url = f"http://127.0.0.1:{PORT}/test/test.txt"
        r1 = self.api.download(base_url, dst=f"{TEST_DIR}/a.txt")
        r2 = self.api.download(base_url, dst=f"{TEST_DIR}/b.txt")
        assert r1.exists()
        assert r2.exists()
        self._assert_no_tmp_files()

    def test_download_no_large_file(self):
        url = f"http://127.0.0.1:{PORT}/test/large.bin"
        dst = f"{TEST_DIR}/large.bin"
        result = self.api.download(url, dst=dst, timeout=30)
        assert result.exists()
        assert result.get_size() == 1 * 1024 * 1024
        self._assert_no_tmp_files()

    def test_download_default_dst(self):
        url = f"http://127.0.0.1:{PORT}/test/test.txt"
        result = self.api.download(url)
        expected_path = "data/download/test.txt"
        assert result.path == expected_path
        assert result.exists()
        result.remove()

    def test_download_custom_dst(self):
        url = f"http://127.0.0.1:{PORT}/test/test.txt"
        dst = f"{TEST_DIR}/custom.bin"
        result = self.api.download(url, dst=dst)
        assert result.path == dst.replace("\\", "/")
        assert result.exists()

    def test_download_with_query_params(self):
        url = f"http://127.0.0.1:{PORT}/test/query?token=abc123"
        result = self.api.download(url)
        expected_path = "data/download/query"
        assert result.path == expected_path
        result.remove()

    def _assert_no_tmp_files(self):
        tmp_dir = "data/tmp"
        if os.path.exists(tmp_dir):
            tmp_files = [f for f in os.listdir(tmp_dir) if f.startswith("download_")]
            assert tmp_files == [], f"临时文件未清理: {tmp_files}"


def clear_tmp_download_files():
    tmp_dir = "data/tmp"
    if os.path.exists(tmp_dir):
        for f in os.listdir(tmp_dir):
            if f.startswith("download_"):
                try:
                    os.remove(os.path.join(tmp_dir, f))
                except Exception:
                    pass


def clear_download_dir():
    download_dir = "data/download"
    if os.path.exists(download_dir):
        for f in os.listdir(download_dir):
            try:
                os.remove(os.path.join(download_dir, f))
            except Exception:
                pass


if __name__ == "__main__":
    import unittest

    unittest.main()
