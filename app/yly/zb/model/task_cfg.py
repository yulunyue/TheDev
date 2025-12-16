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
)
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
    py_name = StrModel("py3")
    docker_image_name = StrModel()

    @property
    def id(self):
        return self.key + "_" + self.name.get_value()

    @property
    def zip_file(self):
        return self.input_dir.child(self.name.get_value() + ".zip")

    def load(self):
        down_load_uri = self.down_load_uri.get_value()
        if not down_load_uri:
            from ..auto import WT, Api

            raise Exception(
                down_load_uri, bool(not down_load_uri), self.name.get_value(), self.key
            )
            uri = WT.get_download_url(self.submit_url.get_value())
            self.down_load_uri.set_value(uri)
            self.save()
        if not self.name.get_value():
            from common.service.api import Api

            f = Api().download(self.down_load_uri.get_value())
            self.name.set_value(f.name)
            self.save()

        self.owner, self.task_id, self.repo, self.pr = get_info_by_name(
            self.name.get_value()
        )
        if not self.docker_image_name.get_value():
            self.docker_image_name.set_value(f"{self.repo}:latest")
        self.input_dir = TASK_DIR.child(self.repo).child(self.key)
        self.input_dir.child("skip.txt").write_if_not_exists("")
        if not self.input_dir.exists():
            from common.service.api import Api

            f = Api().download(self.down_load_uri.get_value())
            f.unzip(self.input_dir)

    @property
    def cg_file(self):
        return self.input_dir.child(self.name.get_value() + ".json")

    @property
    def cg(self):
        return Cg(self.task_id).set_resource(self.cg_file)

    @property
    def py_test_result_json(self):
        return self.input_dir.child(CS.RESULT_JSON_FILE)

    def set_resource(self, resource):
        super().set_resource(resource)
        self.load()
        return self

    def skip(self):
        error_msg = self.error_msg.get_value()
        skip_msg = ""
        if error_msg in {CS.SUCCESS, CS.NOT_FIND_CASES}:
            skip_msg = error_msg
        elif error_msg.startswith("SKIP"):
            skip_msg = error_msg
        return error_msg, skip_msg


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


def query_one(key):
    ret = query_task(key)
    if len(ret) == 1:
        return ret[0]
    raise Exception(key, [d.name for d in ret])


def load_one(key):
    r = query_one(key)
    r.init()
    return r
