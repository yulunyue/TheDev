import os
from common.third_util.io.api import Api
from common.util.export import File
from tests.common.third_util.io.conftest import (
    PORT_BASE,
    TEST_DIR,
    setup_http_server,
    setup_test_dir,
    teardown_test_dir,
    clear_tmp_download_files,
    clear_download_dir,
)


class TestApi:
    """Api 类整合测试"""

    @classmethod
    def setup_class(cls):
        setup_test_dir()
        setup_http_server()
        cls.api = Api("Api")
        cls.api.set_endpoint(f"http://127.0.0.1:{PORT_BASE}")

    @classmethod
    def teardown_class(cls):
        teardown_test_dir()
        clear_tmp_download_files()
        clear_download_dir()

    def setup_method(self):
        clear_tmp_download_files()
        clear_download_dir()

    def teardown_method(self):
        clear_tmp_download_files()
        clear_download_dir()

    def test_http_get_success(self):
        res, ret = self.api.http("GET", "/test/test.txt")
        assert res.status_code == 200
        assert ret == b"Hello World"

    def test_http_post_success(self):
        res, ret = self.api.http("POST", "/test/json", data={"key": "value"})
        assert res.status_code == 200
        assert ret["received"]["key"] == "value"

    def test_http_no_404(self):
        try:
            self.api.http("GET", "/test/error")
        except Exception as e:
            assert "404" in str(e) or "404" in str(e.args)

    def test_download_success(self):
        url = f"http://127.0.0.1:{PORT_BASE}/test/test.txt"
        dst = f"{TEST_DIR}/test.txt"

        result = self.api.download(url, dst=dst)

        assert result.exists()
        assert result.read_data() == b"Hello World"
        self._assert_no_tmp_files()

    def test_download_no_dst_exists(self):
        url = f"http://127.0.0.1:{PORT_BASE}/test/test.txt"
        dst = f"{TEST_DIR}/exist.txt"
        File(dst).write_file(b"pre-existing")

        result = self.api.download(url, dst=dst)

        assert result.read_data() == b"pre-existing"

    def test_download_no_http_404(self):
        url = f"http://127.0.0.1:{PORT_BASE}/test/error"
        dst = f"{TEST_DIR}/error.txt"

        try:
            self.api.download(url, dst=dst)
        except Exception as e:
            assert "404" in str(e) or "404" in str(e.args)
        finally:
            assert not os.path.exists(dst)
            self._assert_no_tmp_files()

    def test_sequential_download(self):
        base_url = f"http://127.0.0.1:{PORT_BASE}/test/test.txt"

        r1 = self.api.download(base_url, dst=f"{TEST_DIR}/a.txt")
        r2 = self.api.download(base_url, dst=f"{TEST_DIR}/b.txt")

        assert r1.exists()
        assert r2.exists()
        self._assert_no_tmp_files()

    def test_download_no_large_file(self):
        url = f"http://127.0.0.1:{PORT_BASE}/test/large.bin"
        dst = f"{TEST_DIR}/large.bin"

        result = self.api.download(url, dst=dst, timeout=60)

        assert result.exists()
        assert result.get_size() == 5 * 1024 * 1024
        self._assert_no_tmp_files()

    def test_download_default_dst(self):
        url = f"http://127.0.0.1:{PORT_BASE}/test/test.txt"

        result = self.api.download(url)

        expected_path = "data/download/test.txt"
        assert result.path == expected_path
        assert result.exists()
        result.remove()

    def test_download_custom_dst(self):
        url = f"http://127.0.0.1:{PORT_BASE}/test/test.txt"
        dst = f"{TEST_DIR}/custom.bin"

        result = self.api.download(url, dst=dst)

        assert result.path == dst.replace("\\", "/")
        assert result.exists()

    def test_download_with_query_params(self):
        url = f"http://127.0.0.1:{PORT_BASE}/test/query?token=abc123"

        result = self.api.download(url)

        expected_path = "data/download/query"
        assert result.path == expected_path
        result.remove()

    def _assert_no_tmp_files(self):
        tmp_dir = "data/tmp"
        if os.path.exists(tmp_dir):
            tmp_files = [f for f in os.listdir(tmp_dir) if f.startswith("download_")]
            assert tmp_files == [], f"临时文件未清理: {tmp_files}"