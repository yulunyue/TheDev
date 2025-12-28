from common.util.export import (
    ToolBase,
    logger,
    File,
    os,
    LOGER_PREFIX,
    List,
    defaultdict,
    Module,
    get_dev_log,
    Dict,
)
from common.tool.export import OsUtil, GC
from .model.export import (
    INPUTS_DIR,
    TASK_DIR,
    get_info_by_name,
    REPO_DIR,
    TaskCfg,
    task_cfg,
    query_task,
    CS,
    get_result,
    DEFAULT_REPO,
    Cg,
    query_one,
)

from .tool.task_docker import DockerTask
from .tool.task_self import SelfTask
from .tool.task_base import ZbTask


def dol(f: TaskCfg, docker_name=None) -> DockerTask:
    if docker_name is not None:
        f.docker_image_name = docker_name
    return DockerTask().set_env(
        f.docker_image_name,
        GC.zb_docker_env.get_value(),
        f.input_dir.child(f"docker_{f.docker_image_name}.log").path,
    )


class ZbMangae(ToolBase):
    def prepare(self, key):
        self.key = key

    def docker(self, name, docker_name=None) -> DockerTask:
        t = query_one(name)

        return dol(t, docker_name).build(t).load()

    def submit(self):
        from .auto import WebTool

        w = WebTool(self.key)
        w.run()

    def build(self):
        for f in query_task(self.key):
            d = dol(f, f.docker_image_name).build(f).load()
            d.docker_build()
            logger.info(f"docker run -it {d.docker_image_name}")

    def clear(self):
        """
        Docstring for clear

        :param self: Description
        需要明确clear的意义和目的
        """
        for t in query_task(self.key):
            t.set_error_msg(CS.FAILED, "unknow")

    def view(self):
        ret: Dict[str, List[TaskCfg]] = defaultdict(list)
        ct = defaultdict(int)
        tasks2 = query_task(self.key)
        for t in tasks2:
            test_ct, code_ct = t.get_result("test"), t.get_result("code")
            key = t.error_msg.get_value().split("=")[0]
            state, msg = key.split(":")
            ret[state, msg].append(t)

        for (state, msg), tasks in ret.items():
            l = get_dev_log(f"data/log/zb/{state}.log")
            l.info(f"\n----{msg} {len(tasks)}----")
            for t in tasks:
                test_ct, code_ct = t.get_result("test"), t.get_result("code")
                l.info(f"id={t.id}; test_ct={test_ct} code_ct={code_ct}")
            l.info("--------------")
            ct[state] += len(tasks)
        self.logger.info(dict(ct))

    def run_all(self, state=""):
        tasks: List[TaskCfg] = []
        tasks2 = query_task(self.key, state=state)
        raise Exception(len(tasks2))
        for f in tasks2:
            f.check()
            if f.can_submit():
                continue
            f.set_error_msg(CS.FAILED, "TODO")
            tasks.append(f)
        for f in tasks:
            t = dol(f)
            logger.run_capture_error(t.run, captures=CS.ZB_TASK_FAIL)
        # owner, task_id, repo, pr = get_info_by_name(f.name)

    def win(self):
        SelfTask().build(query_one(self.key)).run()

    def dev(self):
        self.docker(self.key, "3.9_dev").run()

    def dev1(self):
        self.docker(self.key, "3.9_dev1").run()

    def test(self):
        ZbTask().build(query_one(self.key)).load().apply_test().save()

    def code(self):
        ZbTask().build(query_one(self.key)).apply_code().save()

    def verify(self):
        t = query_one(self.repo, self.key)
        OsUtil("python").run(
            "app/yly/zb/verification1217.py",
            t.input_dir.get_abs_path(),
            t.docker_image_name,
        )

    def pip(self):
        c = SelfTask().build(query_one(self.repo, self.key))
        c.init()
        c.pip()

    def debug(self):
        self.docker().docker_build()
        t = self.docker().make_launch_json()
        t.apply_code()
        vv = self.docker().get_volumn_v(
            {
                t.local_repo.get_abs_path(): t.local_repo.path,
            }
        )
        logger.info(
            f"docker run -p 5678:5678 {vv} -it {self.docker().docker_image_name}"
        )
        logger.info(t.get_py_test_main_code())
        logger.info(
            f"export ZB_PY_TEST_TYPE=code && python -m debugpy --listen 0.0.0.0:5678 --wait-for-client {CS.RUN_VERIFICATION_PY}"
        )

    def search_log(self, search_key='pip install "sqlmesh[bigquery]"'):
        for f in query_task(self.key):
            test_log = f.input_dir.child("test.log")
            if not test_log.exists():
                continue
            datas = test_log.read_file()
            if search_key in datas:
                logger.info(f.resource)
                f.local_packge_extern.set_value(".[dev,bigquery]")
                f.save()

    def files(self):
        for d in REPO_DIR.list_dir(-1):
            pass


if __name__ == "__main__":
    ZbMangae().run()
