from common.util.export import (
    ToolBase,
    logger,
    File,
    os,
    LOGER_PREFIX,
    List,
    defaultdict,
    Module,
)
from common.tool.export import OsUtil, GC
from .model.export import (
    INPUTS_DIR,
    TASK_DIR,
    get_info_by_name,
    INFO_DIR,
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


def dol(f: TaskCfg, docker_image_name) -> DockerTask:
    return DockerTask().set_env(
        docker_image_name,
        GC.zb_docker_env.get_value(),
        f.input_dir.child(f"docker_{docker_image_name}.log").path,
    )


class ZbMangae(ToolBase):
    def prepare(self, repo, key):
        self.key = key
        self.repo = repo

    def task(self, f: ZbTask):
        return f.build(query_one(self.repo, self.key)).load()

    def docker(self, name):
        t = query_one(self.repo, self.key)
        return dol(t, name).build(t).load()

    def local(self):
        return self.task(SelfTask())

    def zb(self):
        return self.task(ZbTask())

    def submit(self):
        from .auto import WebTool

        w = WebTool(self.repo)
        if self.key == "all":
            w.run()
        else:
            w.submit(query_one(self.repo, self.key))

    def build(self):
        for f in query_task(self.repo, self.key):
            d = dol(f, f.docker_image_name).build(f).load()
            d.docker_build()
            logger.info(f"docker run -it {d.docker_image_name}")

    def clear(self):
        """
        Docstring for clear

        :param self: Description
        需要明确clear的意义和目的
        """
        for t in query_task(self.repo, self.key):
            t.set_error_msg(CS.FAILED, "unknow")

    def view(self):
        ret = defaultdict(list)
        tasks2 = query_task(self.repo, self.key)
        for t in tasks2:
            test_ct, code_ct = t.get_result("test"), t.get_result("code")
            key = t.error_msg.get_value().split("=")[0]
            info = dict(id=t.id, test_ct=test_ct, code_ct=code_ct)
            ret[key].append(info)

        msgs = []
        task_num = 0
        for k, tasks in ret.items():
            msgs.append(f"\n----{k} {len(tasks)}----")
            for t in tasks:
                msgs.append(str(t))
            msgs.append("--------------")
            task_num += len(tasks)
        task_view_flie = File("log/zb_task_view.log").write_file("\n".join(msgs))
        self.logger.info(task_view_flie)
        self.logger.info(task_num)

    def main(self):
        tasks = []
        for f in query_task(self.repo, "all"):
            f.check()
            if f.can_submit():
                continue
            f.set_error_msg(CS.FAILED, "TODO")
            tasks.append(f)
        for f in tasks:
            t = dol(f) if GC.zb_docker_env.get_value() else SelfTask()
            t.build(f)
            logger.run_capture_error(t.run, captures=CS.ZB_TASK_FAIL)
        # owner, task_id, repo, pr = get_info_by_name(f.name)

    def test(self):
        self.docker().apply_test().save()

    def code(self):
        self.docker().apply_code().save()

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
        for f in query_task(self.repo, self.key):
            test_log = f.input_dir.child("test.log")
            if not test_log.exists():
                continue
            datas = test_log.read_file()
            if search_key in datas:
                logger.info(f.resource)
                f.local_packge_extern.set_value(".[dev,bigquery]")
                f.save()


if __name__ == "__main__":
    ZbMangae().run()
