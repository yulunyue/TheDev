from common.util.export import logger, File, time
from common.tool.export import ConfigBase, TableBase, StrModel, ListModel, DictModel


INPUTS_DIR = File("app/yly/zb")
TASK_DIR = INPUTS_DIR.child("task")
REPO_BASE = "/testbed"
PASSED = "passed"


def get_info_by_name(file_name: str):
    name, pr = file_name.split("-")
    owner, task_id, repo = name.split("_")
    return owner, task_id, repo, pr


class Cg(ConfigBase):
    base_commit = StrModel()
    pr_url = StrModel()
    repo = StrModel()
    instance_id = StrModel()
    issue_url = StrModel()
    language = StrModel(default_value="python")
    FAIL_TO_PASS = ListModel()
    PASS_TO_PASS = ListModel()
    content_category = StrModel(
        default_value="通用工具"
    )  # 计算、通⽤、⼯具、可视化、系统、时间、⽹络、加密、其他


class TaskCfg(ConfigBase):
    test_main = StrModel()
    setup_env = ListModel()
    result = DictModel()
    after_setup_env = DictModel()
    env = StrModel(default_value="")


TB = TableBase[TaskCfg]().set_resource(INPUTS_DIR.child("all.json"))
