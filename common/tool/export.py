from .task import TASK_MANAGER, get_task, Task
from .thread_util import ThreadRecord
from .os_util import OsUtil
from .base_class.table_base import TableBase, TableConfig
from .base_class.baseconfig import ConfigBase
from .base_class.model import StrModel, NumberModel, DictModel, ListModel, BoolModel
from .bp.node import BpNode
from .mock import Mock
from .bp.compile import BpCompile, BP


class GloablConfg(ConfigBase):
    chrome_driver_path = StrModel("/thedev/data/chrome_driver")
    chrome_driver_uri = StrModel(
        "https://storage.googleapis.com/chrome-for-testing-public/143.0.7499.42/win64/chromedriver-win64.zip"
    )
    chrome_bin_uri = StrModel(
        "https://storage.googleapis.com/chrome-for-testing-public/143.0.7499.42/win64/chrome-win64.zip"
    )
    chrome_bin_path = StrModel(
        "/thedev/data/chrome_bin"
    )  # https://googlechromelabs.github.io/chrome-for-testing/
    git_proxy_prefix = StrModel("")  # https://ghproxy.link/
    BROWSER_USE_API_KEY = StrModel()
    zb_docker_env = StrModel()


GC = GloablConfg("GC").set_resource("gloabl_setting")
