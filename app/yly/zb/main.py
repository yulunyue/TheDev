from common.util.export import (
    ToolBase,
    logger,
    File,
    os,
    LOGER_PREFIX,
    List,
    defaultdict,
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

    def docker(self):
        r: DockerTask = self.task(DockerTask())
        return r.set_env(r.local_cfg.docker_image_name, GC.zb_docker_env.get_value())

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
            w.submit(query_one(self.key))

    def clear(self):
        for t in query_task(self.repo, self.key):
            t.error_msg.set_value(CS.FAILED)
            t.input_dir.child("code.json").remove()
            t.input_dir.child("test.json").remove()
            if t.zip_file.exists():
                logger.info(f"remove {t.zip_file}")
                t.zip_file.remove()
            t.save()

    def zip(self):
        for t in query_task(self.repo, self.key):
            if t.error_msg.get_value() != CS.SUCCESS:
                continue
            result = t.result.get_value()
            if not result[CS.FAIL_TO_PASS]:
                raise Exception(f"No FAIL_TO_PASS {t.id}")
            task = ZbTask().build(t).load()
            task.cfg.PASS_TO_PASS.set_value(result[CS.PASS_TO_PASS])
            task.cfg.FAIL_TO_PASS.set_value(result[CS.FAIL_TO_PASS])
            task.cfg.save()
            t.zip_file.remove()
            t.zip()
            logger.info(t.zip_file)

    def view(self):
        ret = defaultdict(list)
        tasks2 = query_task(self.repo, self.key)
        for t in tasks2:
            key = "NEEDMAKE: " if not t.zip_file.exists() else "NO_NEED: "
            key += t.error_msg.get_value()
            if not t.cg.FAIL_TO_PASS:
                key += f":{CS.NO_FAIL_TO_PASS}"
            _, test_ct = get_result(t.input_dir.child("test.json").path)
            _, code_ct = get_result(t.input_dir.child("code.json").path)
            info = dict(id=t.id, test_ct=test_ct, code_ct=code_ct)
            ret[key].append(info)

        def tmp(v):
            return sum(v["code_ct"].values()) - sum(v["test_ct"].values())

        msgs = []
        for k, tasks in ret.items():
            msgs.append(f"\n----{k} {len(tasks)}----")
            for t in sorted(tasks, key=tmp):
                msgs.append(str(t))
            msgs.append("--------------")
        self.logger.debug("\n".join(msgs))
        self.logger.info(len(tasks2))

    def main(self):
        for f in query_task(self.repo, self.key):
            t = (
                DockerTask().set_env(f.docker_image_name, GC.zb_docker_env.get_value())
                if GC.zb_docker_env.get_value()
                else SelfTask()
            )
            t.build(f)
            logger.run_capture_error(t.run, captures=CS.ZB_TASK_FAIL)
        # owner, task_id, repo, pr = get_info_by_name(f.name)

    def rebuild(self):
        t = self.docker()
        t.dock_util.re_build(t.input_dir.get_abs_path())

    def code(self):
        self.zb().apply_code().save()

    def test(self):
        self.zb().apply_test().save()

    def pip(self):
        self.local.pip()

        c = SelfTask().build(query_one(self.repo, self.key))
        c.init()
        c.pip()

    def debug(self):
        self.apply_code()

    def dev(self):
        pass


if __name__ == "__main__":
    ZbMangae().run()
