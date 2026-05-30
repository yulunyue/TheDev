from .base_class.baseconfig import ConfigBase
from .base_class.base_model import (
    StrModel,
    DictModel,
    ListModel,
    BoolModel,
)
from .base_class.storage.json_config import JsonConfig


class GlobalConfig(JsonConfig):
    chrome_driver_path = StrModel("data/tmp/chrome-data")
    chrome_driver_uri = StrModel(
        default_value="https://storage.googleapis.com/chrome-for-testing-public/150.0.7842.0/linux64/chromedriver-linux64.zip"
    )
    chrome_bin_uri = StrModel(
        default_value="https://storage.googleapis.com/chrome-for-testing-public/150.0.7842.0/linux64/chrome-linux64.zip"
    )
    chrome_bin_path = StrModel(
        default_value="data/tmp/chrome-data"
    )  # https://googlechromelabs.github.io/chrome-for-testing/
    git_proxy_prefix = StrModel("")
    BROWSER_USE_API_KEY = StrModel()
    pip_global_index_url = StrModel()
    pip_trusted_host = StrModel()
    zb_docker_env = StrModel()
    github_token = StrModel()
    npm_path = StrModel(default_value="npm")
    apt_mirror_prefix = StrModel("")
    http_proxy = StrModel("")
    miniconda_mirror = StrModel("")
    conda_channel_prefix = StrModel("")


GlobalConfig.set_resource("config/setting/gloabl_setting.json")
GC = GlobalConfig
