from .util import (
    ConfigBase,
    StrModel,
    ListModel,
    DictModel,
    NumberModel,
    get_info_by_name,
    TASK_DIR,
    CS,
    INFO_DIR,
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
    result = DictModel()
    submit_url = StrModel()
    pr_url = StrModel()
    issue_url = StrModel()
    down_load_uri = StrModel()
    name = StrModel()
    py_name = StrModel()

    def can_skip(self):
        return self.error_msg.get_value().startswith("SKIP:")

    @property
    def docker_image_name(self):
        return f"{self.repo}:{self.py_version}_default"

    @property
    def id(self):
        return self.key + "_" + self.name.get_value()

    @property
    def zip_file(self):
        return self.input_dir.child(self.name.get_value() + ".zip")

    def load(self):
        down_load_uri = self.down_load_uri.get_value()
        if not down_load_uri:
            pass
        if not self.name.get_value():
            from common.third_util.api import Api

            f = Api().download(down_load_uri)
            self.name.set_value(f.name)
            self.save()
        self.task_id = self.key
        self.owner, _, self.repo, self.pr = get_info_by_name(self.name.get_value())
        self.input_dir = TASK_DIR.child(self.repo).child(self.key)
        self.cg = Cg(self.task_id).set_resource(self.cg_file)
        self.local_repo_mock_dir = REPO_DIR.child(self.repo)
        self.py_version = self.py_name.get_value()
        if self.py_version == "py3" or not self.py_version:
            self.py_version = CS.PY_DEFAULT

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

    @property
    def cg_file(self):
        return self.input_dir.child(self.name.get_value() + ".json")

    @property
    def py_test_result_json(self):
        return self.input_dir.child(CS.RESULT_JSON_FILE)

    def zip(self):
        self.zip_file.remove()
        self.input_dir.zip(
            self.zip_file.path, TARGETS + [self.name.get_value() + ".json"]
        )
        return self

    def set_error_msg(self, msg: str):
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
        if len(change_files) >= max_change_files:
            self.set_error_msg(CS.SKIP_CHANGE_FILES_MAX)
        else:
            files = [k for k, v in change_files.items() if v == "test"]
            if isinstance(test_main_values, str) or not test_main_values:
                self.test_main.set_value(files)
            if not self.test_main.get_value():
                self.set_error_msg(f"SKIP: NO_TEST")
        return self

    def get_update_file_by_batch(
        self,
        fp: Patch,
        change_files,
    ):
        for f in fp.get_change_files():
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


def task_cfg(job, task_id):
    f = INFO_DIR.child(job).child(f"{task_id}.json")
    r = TaskCfg(task_id).set_resource(f)
    return r


def query_one(job, key):
    return task_cfg(job, key).load().check()


def query_task(job, key):
    fss = INFO_DIR.child(job).list_dir()
    ret: List[TaskCfg] = []
    for f in fss:
        c = query_one(job, f.name)
        # if c.repo != job:
        #     continue
        if key != "all" and key not in c.id:
            continue
        ret.append(c)
    return ret
