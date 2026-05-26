import sys
from common.util.export import File, logger
from common.third_util.io.api import Api

CHROME_DATA_DIR = "data/chrome"
USER_DATA_DIR = "data/chrome/user-data"

CHROME_DRIVER_PATH = "data/tmp/chrome-data"
CHROME_DRIVER_URI = "https://storage.googleapis.com/chrome-for-testing-public/150.0.7842.0/linux64/chromedriver-linux64.zip"
CHROME_BIN_PATH = "data/tmp/chrome-data"
CHROME_BIN_URI = "https://storage.googleapis.com/chrome-for-testing-public/150.0.7842.0/linux64/chrome-linux64.zip"


class SeleniumConfig:
    chrome_driver_path = CHROME_DRIVER_PATH
    chrome_driver_uri = CHROME_DRIVER_URI
    chrome_bin_path = CHROME_BIN_PATH
    chrome_bin_uri = CHROME_BIN_URI

    @staticmethod
    def get_platform() -> tuple:
        if sys.platform.startswith("win"):
            return "win64", "chrome.exe", "chromedriver.exe"
        elif sys.platform.startswith("linux"):
            return "linux64", "chrome", "chromedriver"
        elif sys.platform.startswith("darwin"):
            return "mac-arm64", "chrome", "chromedriver"
        return "linux64", "chrome", "chromedriver"

    @staticmethod
    def ensure_platform_url(uri: str, platform_name: str) -> str:
        parts = uri.split("/")
        for i, p in enumerate(parts):
            if p.endswith("-win64"):
                parts[i] = p.replace("-win64", f"-{platform_name}")
            elif p.endswith("-mac-arm64") or p.endswith("-linux64"):
                pass
        return "/".join(parts)

    @staticmethod
    def ensure_chrome() -> tuple:
        chrome_exe = File(SeleniumConfig.chrome_bin_path)
        chrome_driver = File(SeleniumConfig.chrome_driver_path)
        platform_name, chrome_name, driver_name = SeleniumConfig.get_platform()

        if not chrome_exe.exists():
            uri = SeleniumConfig.ensure_platform_url(
                SeleniumConfig.chrome_bin_uri, platform_name
            )
            Api().download(uri).unzip(chrome_exe.path)
        if not chrome_driver.exists():
            uri = SeleniumConfig.ensure_platform_url(
                SeleniumConfig.chrome_driver_uri, platform_name
            )
            Api().download(uri).unzip(chrome_driver.path)
        if not chrome_exe.exists() or not chrome_driver.exists():
            raise Exception(
                f"Chrome or ChromeDriver 下载失败: {chrome_exe.path} {chrome_driver.path}"
            )

        chrome_exe_file = chrome_exe.child(f"chrome-{platform_name}/{chrome_name}")
        chrome_driver_file = chrome_driver.child(
            f"chromedriver-{platform_name}/{driver_name}"
        )
        return chrome_exe_file, chrome_driver_file
