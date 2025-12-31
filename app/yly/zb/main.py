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

from .tool.task_docker import DockerTask, get_volumn_v
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

    def docker(self, name=None, docker_name=None) -> DockerTask:
        if name is None:
            name = self.key
        t = query_one(name)
        return dol(t, docker_name).build(t).load()

    def submit(self):
        from .auto import WebTool

        w = WebTool(self.key)
        w.run()

    def build(self):
        d = self.docker()
        d.apply_test()
        d.docker_build()
        logger.info(f"docker run -it {d.docker_image_name}")

    def clear(self):
        """
        Docstring for clear

        :param self: Description
        需要明确clear的意义和目的
        """
        for t in query_task(self.key, state=CS.DOCKER_BUILD_FAILED):
            # print(t.cg_file)
            t.set_error_msg(CS.ERROR, CS.DOCKER_BUILD_FAILED)

    def check(self):
        for t in query_task(self.key, state=CS.SUCCESS):
            t.set_error_msg(CS.SUCCESS, "CHECKING")
            dol(t, "check").build(t).run()

    def view(self):
        ret: Dict[str, List[TaskCfg]] = defaultdict(list)
        ct = defaultdict(int)
        tasks2 = query_task(self.key)
        for t in tasks2:
            test_ct, code_ct = t.get_result("test"), t.get_result("code")
            key = t.error_msg.get_value().split("=")[0]
            start_idx = key.index(":")
            state, msg = key[:start_idx], key[start_idx + 1 :]
            ret[state, msg].append(t)

        def u(name, ct):
            ret = []
            for k, v in ct.items():
                ret.append(f"{name}_{k}={v}")
            return " ".join(ret)

        for (state, msg), tasks in ret.items():
            l = get_dev_log(f"data/log/zb/{state}.log")
            l.info(f"\n----{msg} {len(tasks)}----")
            for t in tasks:
                test_ct, code_ct = t.get_result("test"), t.get_result("code")
                l.info(f"id={t.id}; {u('test',test_ct)} {u('code',code_ct)}")
            l.info("--------------")
            ct[state] += len(tasks)
        self.logger.info(dict(ct))

    def exec(self, state=""):
        tasks: List[TaskCfg] = []
        tasks2 = query_task(self.key, state=state)
        for f in tasks2:
            f.check()
            s, b, *args = f.error_msg.get_value().split(":")
            if s == CS.FAILED:
                f.set_error_msg(CS.FAILED, "WAIT")
                tasks.append(f)
        for f in tasks:
            t = dol(f).build(f)
            logger.run_capture_error(t.run, captures=CS.ZB_TASK_FAIL)
        # owner, task_id, repo, pr = get_info_by_name(f.name)

    def dev(self, env=None):
        t = query_one(self.key).set_env(env)
        dol(t).build(t).run()

    def win(self):
        SelfTask().build(query_one(self.key)).run()

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

    def debug(self, name):
        t = self.docker(docker_name="debug")
        if name == "test":
            t.apply_test()
        elif name == "code":
            t.apply_code()
        else:
            raise Exception(name)
        t.make_launch_json()
        logger.info(t.get_py_test_main_code())
        t.docker_build()
        vv = t.get_volumn_v(
            {
                t.local_repo.get_abs_path(): t.local_repo.path,
            }
        )
        logger.info(
            f"docker run -p 5678:5678 {vv} -it {self.docker().docker_image_name}"
        )

        logger.info(
            f"python -m debugpy --listen 0.0.0.0:5678 --wait-for-client py_test_main.py"
        )

    def log(self, name=None):
        search_key = """
E             'Flags' object has no attribute 'state_modified_compare_more_unrendered_values'


""".replace(
            "\n", ""
        )
        for f in query_task(self.key):
            test_log = f.input_dir.child("code.log")
            # test_log = f.input_dir.child("docker_sqlmesh_3.9_default.log")
            if not test_log.exists():
                continue
            datas = test_log.read_file()
            idx = datas.find(search_key)
            if idx != -1:
                f.set_env(name)
                # f.set_error_msg(CS.FAILED, search_key)
                logger.info(
                    f"{f.resource}->{f.error_msg.get_value()} log->{datas[idx:idx+100]}"
                )

    def files(self):
        for d in REPO_DIR.list_dir(-1):
            pass


if __name__ == "__main__":
    ZbMangae().run()
