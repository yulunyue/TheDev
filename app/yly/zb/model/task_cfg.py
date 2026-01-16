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
from common.tool.export import StrUtil
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
        if err_msg.startswith(CS.FAILED) or err_msg.startswith(CS.RUN):
            return False
        return True

    @property
    def id(self):
        return f"{self.env_name}/{self.name.get_value()}_{self.task_id}_{self.error_msg.get_value()[:15]}"

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

    def set_env(self, env: str):
        if env == self.env_name or env is None:
            return self
        py_ver = float(env.split("_")[0])
        if py_ver < 2.7 or py_ver > 3.99:
            env = "3.9_" + env
        env_dir = REPO_DIR.child(self.repo).child(env)
        env_names = [
            f.file_name
            for f in REPO_DIR.child(self.repo).list_dir(with_dir=True)
            if f.is_dir()
        ]
        logger.info(f"{self.env_name}->{env}")
        pr = env_dir.child("pr")
        if not pr.exists():
            input(f"are you sure new env not {env_names}")
            pr.make_dir_if_not_exist(True)
            d = REPO_DIR.child(self.repo, self.env_name, CS.SETUP_ENV_SH).copy_to(
                env_dir.child(CS.SETUP_ENV_SH)
            )
            input(f"do {d}")
        dst = pr.child(self.resource.file_name)
        self.resource.move_to(dst)
        self.set_resource(dst).load()
        return self

    @property
    def cg_file(self):
        return self.input_dir.child(self.name.get_value() + ".json")

    @property
    def py_test_result_json(self):
        return self.input_dir.child(CS.RESULT_JSON_FILE)

    def zip(self):
        result = self.result.get_value()
        if self.error_msg.get_value().startswith(CS.SUCCESS):
            if not result[CS.PASS_TO_PASS] or not result[CS.FAIL_TO_PASS]:
                raise Exception(self.id, result)
            self.cg.PASS_TO_PASS.set_value(result[CS.PASS_TO_PASS])
            self.cg.FAIL_TO_PASS.set_value(result[CS.FAIL_TO_PASS])
        self.cg.save()
        self.zip_file.remove()
        self.input_dir.zip(
            self.zip_file.path, TARGETS + [self.name.get_value() + ".json"]
        )
        return self

    def set_uri(self, current_url, download_url: str, task_id):
        name = download_url.split("/").pop().split("?")[0].split(".zip")[0]
        self.task_id = task_id
        self.owner, _, self.repo, self.pr = get_info_by_name(name)
        self.set_resource(REPO_DIR.child(f"{self.repo}/3.9_default/pr/{self.pr}.json"))
        self.name.set_value(name)
        self.submit_url.set_value(current_url)
        self.down_load_uri.set_value(download_url)
        self.set_error_msg(CS.FAILED, "TODO")
        self.save()

    def set_error_msg(self, state, msg: str):
        if state not in {CS.SUCCESS, CS.SKIPPED, CS.FAILED, CS.ERROR, CS.RUN}:
            raise Exception(msg)
        msg = f"{state}:{msg}"
        if msg != self.error_msg.get_value():
            logger.info(f"{self.name.get_value()}->{self.error_msg.get_value()}=>{msg}")
            self.error_msg.set_value(msg)
            self.save()
        return self

    def add_error_msg_flag(self, flag):
        msg = self.error_msg.get_value()
        if flag not in msg:
            logger.info(f"{self.name.get_value()}->{msg}+{flag}")
            self.error_msg.set_value(msg + flag)
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

    def __repr__(self):
        return self.id


def task_cfg(f: File):
    raise Exception("todo")


def get_map():
    if not TaskCfg.TASK_CFGS_MAP:
        d: Dict[str, TaskCfg] = dict()
        fss = REPO_DIR.list_dir(depth=5)
        for f in fss:
            if "/pr/" in f.path and f.path.endswith(".json"):
                t = TaskCfg(f.path).set_resource(f).load()
                if t.task_id in d:
                    raise Exception(t.id, d[t.task_id].id)
                d[t.task_id] = t
        TaskCfg.TASK_CFGS_MAP = d
    return TaskCfg.TASK_CFGS_MAP


def query_task(key: str = ""):
    ret: List[TaskCfg] = []
    tasks: List[TaskCfg] = sorted(
        get_map().values(), key=lambda x: [x.repo, x.env_name, x.pr]
    )
    for v in tasks:
        # logger.info([v.id, key in v.id or key == "all"])
        if not key or StrUtil().set_matchs([key]).match(v.id):
            ret.append(v)
    return ret


def query_one(key):
    res = query_task(key)
    if len(res) == 1:
        return res[0]
    raise Exception(key, res)


def new_one(key):
    m = get_map()
    if key not in m:
        m[key] = TaskCfg(key)
    return m[key]
