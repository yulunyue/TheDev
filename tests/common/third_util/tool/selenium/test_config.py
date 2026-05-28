import sys
from common.third_util.tool.selenium.config import SeleniumConfig


class TestSeleniumConfig:

    def test_get_platform_win(self):
        original_platform = sys.platform
        platform_name, chrome_name, driver_name = SeleniumConfig.get_platform()
        if original_platform.startswith("win"):
            assert platform_name == "win64"
            assert chrome_name == "chrome.exe"
            assert driver_name == "chromedriver.exe"
        elif original_platform.startswith("linux"):
            assert platform_name == "linux64"
            assert chrome_name == "chrome"
            assert driver_name == "chromedriver"

    def test_get_base_paths(self):
        chrome_driver_path, chrome_bin_path = SeleniumConfig._get_base_paths()
        if sys.platform.startswith("win"):
            assert "chrome_driver" in chrome_driver_path
            assert "chrome_bin" in chrome_bin_path
        else:
            assert chrome_driver_path == "/thedev/data/"
            assert chrome_bin_path == "/thedev/data/"

    def test_ensure_chrome_paths_exist(self):
        chrome_exe_file, chrome_driver_file = SeleniumConfig.ensure_chrome()
        assert chrome_exe_file.exists()
        assert chrome_driver_file.exists()

    def test_ensure_chrome_exe_valid(self):
        chrome_exe_file, chrome_driver_file = SeleniumConfig.ensure_chrome()
        assert chrome_exe_file.path.endswith("chrome.exe") or chrome_exe_file.path.endswith("chrome")

    def test_ensure_chrome_driver_valid(self):
        chrome_exe_file, chrome_driver_file = SeleniumConfig.ensure_chrome()
        assert chrome_driver_file.path.endswith("chromedriver.exe") or chrome_driver_file.path.endswith("chromedriver")

    def test_ensure_platform_url(self):
        uri = "https://example.com/chromedriver-win64.zip"
        result = SeleniumConfig.ensure_platform_url(uri, "linux64")
        assert "linux64" in result
        assert "win64" not in result