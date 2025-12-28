from .util import (
    ConfigBase,
    StrModel,
    ListModel,
    DictModel,
    NumberModel,
    get_info_by_name,
    TASK_DIR,
    CS,
    REPO_DIR,
    Cg,
    TARGETS,
    REPO_BASE,
)
from .repo_cg import RepoCg
from common.util.export import List, Dict, File, logger
from common.third_service.git_tool.git_util import GitUtil, Patch


class TaskCfg(ConfigBase):
    test_main = ListModel()
    error_msg = StrModel()
    depends_models = DictModel()
    result = DictModel()
    submit_url = StrModel()
    pr_url = StrModel()
    issue_url = StrModel()
    down_load_uri = StrModel()
    name = StrModel()
    local_packge_extern = StrModel()
    TASK_CFGS_MAP: Dict[str, "TaskCfg"] = None

    def get_local_packge_extern(self):
        value = self.local_packge_extern.get_value()
        if value:
            return value
        value = self.global_confg.local_packge_extern.get_value()
        if not value:
            value = "."
        return value

    def can_submit(self):
        err_msg = self.error_msg.get_value()
        if err_msg.startswith(CS.SUCCESS):
            return True
        if err_msg.startswith(CS.SKIPPED):
            info = err_msg.split(f"{CS.SKIPPED}:").pop().split("=")[0]
            if info not in CS.SKIP_MAP:
                raise Exception(
                    self.task_id,
                    self.name.get_value(),
                    err_msg,
                    list(CS.SKIP_MAP.keys()),
                )
            return True
        return False

    @property
    def id(self):
        return f"{self.name.get_value()}_{self.task_id}"

    @property
    def zip_file(self):
        return self.input_dir.child(self.name.get_value() + ".zip")

    def load(self):
        down_load_uri = self.down_load_uri.get_value()
        submit_uri = self.submit_url.get_value()
        if not down_load_uri or not submit_uri:
            raise Exception(self.resource)
        self.task_id = submit_uri.split("recordId=").pop().split("&")[0]
        if not self.name.get_value():
            from common.third_util.api import Api

            f = Api().download(down_load_uri)
            self.name.set_value(f.name)
            self.save()
        info = self.resource.path.replace(REPO_DIR.path + "/", "").split("/")
        self.env_name = info[1]
        self.py_version = self.env_name.split("_")[0]
        self.owner, _, self.repo, self.pr = get_info_by_name(self.name.get_value())
        self.docker_image_name = f"{self.repo}:{self.env_name}"
        self.input_dir = TASK_DIR.child(self.repo).child(self.task_id)
        self.cg = Cg(self.task_id).set_resource(self.cg_file)
        self.local_repo_mock_dir = REPO_DIR.child(self.repo)
        self.env_dir = self.local_repo_mock_dir.child(self.env_name)
        self.global_confg: RepoCg = RepoCg.new(
            self.repo, self.local_repo_mock_dir.child("config.json")
        )
        if not self.input_dir.exists():
            raise Exception(self.input_dir)
            from common.third_util.api import Api

            f = Api().download(self.down_load_uri.get_value())
            f.unzip(self.input_dir)
        self.pr_url.set_value(self.cg.pr_url.get_value())
        self.repo_uri = self.pr_url.get_value().split("/pull")[0] + ".git"
        self.issue_url.set_value(self.cg.issue_url.get_value())
        self.git_cmd = self.cg.get_git_util()
        self.pr_util = self.git_cmd.get_pr(self.pr)
        self.test_patch = self.pr_util.get_patch(self.input_dir.child("test.patch"))
        self.code_patch = self.pr_util.get_patch(self.input_dir.child("code.patch"))
        self.local_repo = File(f"{REPO_BASE}/{self.owner}/{self.repo}")
        return self

    @property
    def cg_file(self):
        return self.input_dir.child(self.name.get_value() + ".json")

    @property
    def py_test_result_json(self):
        return self.input_dir.child(CS.RESULT_JSON_FILE)

    def zip(self):
        result = self.result.get_value()
        self.cg.PASS_TO_PASS.set_value(result[CS.PASS_TO_PASS])
        self.cg.FAIL_TO_PASS.set_value(result[CS.FAIL_TO_PASS])
        self.zip_file.remove()
        self.input_dir.zip(
            self.zip_file.path, TARGETS + [self.name.get_value() + ".json"]
        )
        return self

    def set_error_msg(self, state, msg: str):
        if state not in {CS.SUCCESS, CS.SKIPPED, CS.FAILED}:
            raise Exception(msg)
        msg = f"{state}:{msg}"
        if msg != self.error_msg.get_value():
            logger.info(f"{self.name.get_value()}->{self.error_msg.get_value()}=>{msg}")
            self.error_msg.set_value(msg)
            self.save()
        return self

    def check(self):
        test_main_values = self.test_main.get_value()
        change_files: Dict[str, str] = dict()
        max_change_files = 20
        for p in [self.test_patch, self.code_patch]:
            self.get_update_file_by_batch(p, change_files)
        if change_files.get("has_bin"):
            self.set_error_msg(CS.SKIPPED, CS.HAS_HEX_FILES)
        elif len(change_files) >= max_change_files:
            self.set_error_msg(
                CS.SKIPPED,
                f"{CS.CHANGE_FILES_TOO_MAX}={len(change_files)}>={max_change_files}",
            )
        else:
            files = [k for k, v in change_files.items() if v == "test"]
            if isinstance(test_main_values, str) or not test_main_values:
                self.test_main.set_value(files)
            if not self.test_main.get_value():
                self.set_error_msg(CS.SKIPPED, CS.NOT_FIND_CASES)
        return self

    def get_update_file_by_batch(
        self,
        fp: Patch,
        change_files,
    ):
        for f in fp.get_change_files():
            if f.local.file_name.endswith(".png"):
                change_files["has_bin"] = True
            if not f.local.file_name.endswith(".py"):
                continue
            key = f.filename
            if f.local.file_name.startswith("test_"):
                change_files[key] = "test"
            else:
                change_files[key] = "code"

    def get_result(self, key):
        ret = dict()
        results = self.result.get_value()
        if key not in results:
            return dict(no=-1)
        for k, v in self.result.get_value()[key].items():
            ret[v] = ret.get(v, 0) + 1
        return ret


def task_cfg(f: File):
    name = f
    if isinstance(f, File):
        name = f.path
    r = TaskCfg(name).set_resource(f).load()
    return r


def query_one(key):
    ret = query_task(key)
    if len(ret) == 1:
        return ret[0]
    raise Exception(ret)


def query_task(key: str):
    if not TaskCfg.TASK_CFGS_MAP:
        TaskCfg.TASK_CFGS_MAP = dict()
        fss = REPO_DIR.list_dir(depth=3)
        for f in fss:
            if "/pr/" in f.path:
                t = task_cfg(f)
                TaskCfg.TASK_CFGS_MAP[t.id] = t
    ret: List[TaskCfg] = []
    for k, v in TaskCfg.TASK_CFGS_MAP.items():
        if key in k:
            ret.append(v)
    return ret
