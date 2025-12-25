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


class ZbMangae(ToolBase):
    def prepare(self, repo, key):
        self.key = key
        self.repo = repo

    def task(self, f: ZbTask):
        return f.build(query_one(self.repo, self.key)).load()

    _docker: DockerTask = None

    def docker(self):
        if self._docker is None:
            self._docker: DockerTask = self.task(DockerTask())
            self._docker.set_env(
                self._docker.local_cfg.docker_image_name, GC.zb_docker_env.get_value()
            )
        return self._docker

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
            DockerTask().set_env(
                f.docker_image_name, GC.zb_docker_env.get_value()
            ).build(f).load().docker_build()
            logger.info(f"docker run -it {self.docker().docker_image_name}")

    def clear(self):
        """
        Docstring for clear

        :param self: Description
        需要明确clear的意义和目的
        """
        for t in query_task(self.repo, self.key):
            t.set_error_msg(CS.FAILED)
            t.check()

    def check(self):
        for t in query_task(self.repo, self.key):
            t.check()
            t.save()
        self.view()

    def view(self):
        ret = defaultdict(list)
        tasks2 = query_task(self.repo, self.key)
        for t in tasks2:
            key = t.error_msg.get_value().split("=")[0]
            result = t.result.get_value()
            fail_to_pass = (
                "HAS_FAIL_TO_PASS"
                if len(result.get(CS.FAIL_TO_PASS, [])) != 0
                else "NO_FAIL_TO_PASS"
            )
            for v in t.test_main.get_value():
                if "::" in v:
                    logger.info(t.resource)
            test_ct, code_ct = t.get_result("test"), t.get_result("code")
            if not t.error_msg.get_value().startswith("SKIP:"):
                if code_ct.get("error"):
                    key = f"{fail_to_pass}_NEED_CHECK_WITH_CODE_ERROR"
                    t.set_error_msg(key)
                elif code_ct.get("failed"):
                    key = f"{fail_to_pass}_NEED_CHECK_WITH_CODE_FAILED"
                    t.set_error_msg(key)
            info = dict(id=t.id, test_ct=test_ct, code_ct=code_ct)
            ret[key].append(info)

        def tmp(v):
            return sum(v["code_ct"].values()) + sum(v["test_ct"].values())

        msgs = []
        for k, tasks in ret.items():
            msgs.append(f"\n----{k} {len(tasks)}----")
            for t in sorted(tasks, key=tmp):
                msgs.append(str(t))
            msgs.append("--------------")
        task_view_flie = File("log/zb_task_view.log")
        self.logger.info(task_view_flie)
        task_view_flie.write_file("\n".join(msgs))
        self.logger.info(len(tasks2))

    def main(self):
        for f in query_task(self.repo, self.key):
            err_msg = f.error_msg.get_value()
            if err_msg == CS.SUCCESS or err_msg.startswith("SKIP:"):
                continue
            t = (
                DockerTask().set_env(f.docker_image_name, GC.zb_docker_env.get_value())
                if GC.zb_docker_env.get_value()
                else SelfTask()
            )
            t.build(f)
            logger.run_capture_error(t.run, captures=CS.ZB_TASK_FAIL)
        # owner, task_id, repo, pr = get_info_by_name(f.name)

    def test(self):
        self.docker().apply_test().save()

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


if __name__ == "__main__":
    ZbMangae().run()
