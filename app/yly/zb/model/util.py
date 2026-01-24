from common.util.export import logger, File, time, List
from common.tool.export import (
    ConfigBase,
    TableBase,
    NumberModel,
    StrModel,
    ListModel,
    DictModel,
    BoolModel,
)
from ..template.run_verification import CS, get_result
from common.third_service.git_tool.git_util import GitUtil, Patch

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
REPO_DIR = INPUTS_DIR.child("repo")
DEFAULT_REPO = "briefcase"


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

    def set_resource(self, resource):
        ret = super().set_resource(resource)
        repo_dir = REPO_DIR.child(self.repo.get_value().split("/").pop()).child(
            self.instance_id.get_value()
        )
        self.test_patch_file = repo_dir.child("test.patch")
        self.code_patch_file = repo_dir.child("code.patch")
        return ret

    def clone_patch(self):
        self.test_patch_file.write_file(self.test_patch.get_value())
        self.code_patch_file.write_file(self.patch.get_value())

    def get_git_util(self):
        repo = File(f"{REPO_BASE}/{self.repo.get_value()}").make_dir_if_not_exist()
        return (
            GitUtil()
            .set_repo_url(self.pr_url.get_value().split("/pull")[0] + ".git")
            .clone()
        )
