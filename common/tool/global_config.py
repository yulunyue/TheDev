from .base_class.baseconfig import ConfigBase
from .base_class.base_model import (
    StrModel,
    DictModel,
    ListModel,
    BoolModel,
)
from .base_class.storage.json_config import JsonConfig


class GlobalConfig(JsonConfig):
    chrome_driver_path = StrModel("/thedev/data/chrome_driver")
    chrome_driver_uri = StrModel(
        default_value="https://storage.googleapis.com/chrome-for-testing-public/143.0.7499.42/win64/chromedriver-win64.zip"
    )
    chrome_bin_uri = StrModel(
        default_value="https://storage.googleapis.com/chrome-for-testing-public/143.0.7499.42/win64/chrome-win64.zip"
    )
    chrome_bin_path = StrModel(
        default_value="/thedev/data/chrome_bin"
    )  # https://googlechromelabs.github.io/chrome-for-testing/
    git_proxy_prefix = StrModel("")  # https://ghproxy.link/
    BROWSER_USE_API_KEY = StrModel()
    pip_global_index_url = StrModel()
    pip_trusted_host = StrModel()
    zb_docker_env = StrModel()
    github_token = StrModel()
    npm_path = StrModel(default_value="npm")


GlobalConfig.set_resource("config/setting/gloabl_setting.json")
GC = GlobalConfig
