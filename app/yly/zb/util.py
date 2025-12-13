from common.util.export import logger, File, time
from common.tool.export import (
    ConfigBase,
    TableBase,
    StrModel,
    ListModel,
    DictModel,
    BoolModel,
)
from .run_verification import CS

TARGETS = [
    CS.CODE_PATCH,
    CS.TEST_PATCH,
    CS.RUN_VERIFICATION_PY,
    CS.DOCKERFILE,
    CS.SETUP_ENV_SH,
    CS.SETUP_REPO_SH,
]
INPUTS_DIR = File("app/yly/zb")
TASK_DIR = INPUTS_DIR.child("task")
INFO_DIR = INPUTS_DIR.child("info")


class GConfig(ConfigBase):
    repo_path = StrModel(default_value="/testbed")


GC = GConfig("zb").set_resource("zb")
REPO_BASE = GC.repo_path.get_value()


def get_info_by_name(file_name: str):
    try:
        heads = file_name.split("-")
        pr = heads.pop()
        name = "-".join(heads)
        owner, task_id, repo = name.split("_")
        return owner, task_id, repo, pr
    except Exception as e:
        raise Exception(e, file_name)


class Cg(ConfigBase):
    base_commit = StrModel()
    pr_url = StrModel()
    repo = StrModel()
    instance_id = StrModel()
    issue_url = StrModel()
    language = StrModel(default_value="python")
    FAIL_TO_PASS = ListModel()
    test_patch = StrModel()
    patch = StrModel()
    PASS_TO_PASS = ListModel()
    content_category = StrModel(
        default_value="通用工具"
    )  # 计算、通⽤、⼯具、可视化、系统、时间、⽹络、加密、其他


class TaskCfg(ConfigBase):
    test_main = StrModel()
    error_msg = StrModel()
    skip = BoolModel()
    setup_env = ListModel()
    result = DictModel()
    after_setup_env = DictModel()
    need_setup_env = BoolModel(False)
    submit_url = StrModel()
    upload_uri = StrModel()
    pr_url = StrModel()
    issue_url = StrModel()
    down_load_uri = StrModel()
    name = StrModel()


def task_cfg(task_id):
    f = INFO_DIR.child(f"{task_id}.json")
    return TaskCfg(task_id).set_resource(f)
