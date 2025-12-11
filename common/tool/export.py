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
    chrome_bin_path = StrModel(
        "data/chrome_bin"
    )  # https://googlechromelabs.github.io/chrome-for-testing/
    git_proxy_prefix = StrModel("")  # https://ghproxy.link/


GC = GloablConfg("GC").set_resource("gloabl_setting")
