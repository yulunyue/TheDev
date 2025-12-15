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
from .run_verification import CS, get_result

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


class TaskCfg(ConfigBase):
    test_main = StrModel()
    error_msg = StrModel()
    setup_env = ListModel()
    result = DictModel()
    after_setup_env = DictModel()
    submit_url = StrModel()
    pr_url = StrModel()
    pr_change_files = NumberModel()
    issue_url = StrModel()
    down_load_uri = StrModel()
    name = StrModel()
    skip = StrModel()
    py_name = StrModel("py3")
    docker_image_name = StrModel()

    @property
    def id(self):
        return self.key + "_" + self.name.get_value()

    @property
    def zip_file(self):
        return self.input_dir.child(self.name.get_value() + ".zip")

    def load(self):

        if not self.down_load_uri.get_value():
            from .auto import WT, Api

            uri = WT.get_download_url(self.submit_url.get_value())
            self.down_load_uri.set_value(uri)
            self.save()
        if not self.name.get_value():
            from common.service.api import Api

            f = Api().download(self.down_load_uri.get_value())
            self.name.set_value(f.name)
            self.save()

        self.owner, task_id, self.repo, self.pr = get_info_by_name(
            self.name.get_value()
        )
        if not self.docker_image_name.get_value():
            self.docker_image_name.set_value(f"{self.repo}:latest")
        self.input_dir = TASK_DIR.child(self.repo).child(self.key)
        if not self.input_dir.exists():
            from common.service.api import Api

            f = Api().download(self.down_load_uri.get_value())
            f.unzip(self.input_dir)

    @property
    def cg_file(self):
        return self.input_dir.child(self.name.get_value() + ".json")

    @property
    def py_test_result_json(self):
        return self.input_dir.child(CS.RESULT_JSON_FILE)

    def set_resource(self, resource):
        super().set_resource(resource)
        self.load()
        return self


def task_cfg(task_id):
    f = INFO_DIR.child(f"{task_id}.json")
    r = TaskCfg(task_id).set_resource(f)
    return r


def query_task(key=""):
    fss = INFO_DIR.list_dir()
    ret: List[TaskCfg] = []
    for f in fss:
        c = task_cfg(f.name)
        if key and key not in c.id:
            continue
        ret.append(c)
    return ret
