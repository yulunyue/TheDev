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
)
from .repo_cg import RepoCg
from common.util.export import List


class TaskCfg(ConfigBase):
    test_main = ListModel()
    error_msg = StrModel()
    result = DictModel()
    after_setup_env = DictModel()
    submit_url = StrModel()
    pr_url = StrModel()
    issue_url = StrModel()
    down_load_uri = StrModel()
    name = StrModel()
    py_name = StrModel()

    @property
    def docker_image_name(self):
        py_version = self.get_python_version()
        return f"{self.repo}:{py_version}"

    @property
    def id(self):
        return self.key + "_" + self.name.get_value()

    @property
    def zip_file(self):
        return self.input_dir.child(self.name.get_value() + ".zip")

    @property
    def repo_cg(self) -> RepoCg:
        return RepoCg.new(self.repo, REPO_DIR.child(f"{self.repo}/default_config.json"))

    def get_python_version(self):
        if self.py_name.get_value():
            return self.py_name.get_value()
        if self.repo_cg.py_name.get_value():
            return self.repo_cg.py_name.get_value()
        return "3.9_default"

    def load(self):
        down_load_uri = self.down_load_uri.get_value()
        if not down_load_uri:
            raise Exception("xx")
        if not self.name.get_value():
            from common.service.api import Api

            f = Api().download(down_load_uri)
            self.name.set_value(f.name)
            self.save()

        self.owner, self.task_id, self.repo, self.pr = get_info_by_name(
            self.name.get_value()
        )
        if self.py_name.get_value() == "py3":
            self.py_name.set_value("")
        self.input_dir = TASK_DIR.child(self.repo).child(self.key)
        if not self.input_dir.exists():
            from common.service.api import Api

            f = Api().download(self.down_load_uri.get_value())
            f.unzip(self.input_dir)
        return self

    @property
    def cg_file(self):
        return self.input_dir.child(self.name.get_value() + ".json")

    @property
    def cg(self):
        return Cg(self.task_id).set_resource(self.cg_file)

    @property
    def py_test_result_json(self):
        return self.input_dir.child(CS.RESULT_JSON_FILE)

    def skip(self):
        error_msg = self.error_msg.get_value()
        skip_msg = ""
        if error_msg in {CS.SUCCESS, CS.NOT_FIND_CASES}:
            skip_msg = error_msg
        elif error_msg.startswith("SKIP"):
            skip_msg = error_msg
        return error_msg, skip_msg

    def zip(self):
        self.input_dir.zip(
            self.zip_file.path, TARGETS + [self.name.get_value() + ".json"]
        )
        return self


def task_cfg(job, task_id):
    f = INFO_DIR.child(job).child(f"{task_id}.json")
    r = TaskCfg(task_id).set_resource(f)
    return r


def query_one(job, key):
    return task_cfg(job, key).load()


def query_task(job, key):
    fss = INFO_DIR.child(job).list_dir()
    ret: List[TaskCfg] = []
    for f in fss:
        c = query_one(job, f.name)
        if key != "all" and key not in c.id:
            continue
        ret.append(c)
    return ret
