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
from app.yly.zb.model.export import (
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
from .auto import WebTool


def dol(f: TaskCfg, docker_name=None) -> DockerTask:
    if docker_name is not None:
        f.docker_image_name = docker_name
    return DockerTask().set_env(
        f.docker_image_name,
        GC.zb_docker_env.get_value(),
        f.input_dir.child(f"docker_{f.docker_image_name}.log").path,
    )


class ZbMangae:

    def docker(self, name=None, docker_name=None) -> DockerTask:
        if name is None:
            name = self.key
        t = query_one(name)
        return dol(t, docker_name).build(t).load()

    def task_update(self, use_local=True):
        f = File("data/zb/task.json")
        if use_local:
            data = f.read_file()
        else:
            w = WebTool()
            data = w.get_all_task()
        f.write_file(data)
        logger.info(f)
        for k in data:
            t = query_one(k)
            t.add_error_msg_flag(CS.REJECT)

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
        for k in []:
            # for t in query_task(self.key):
            # print(t.cg_file)
            if not k:
                continue
            t = query_one(k)
            t.set_error_msg(CS.SKIPPED, CS.ISSUE_0)

    def check(self):
        for t in query_task(self.key, state=CS.FAILED):
            DockerTask().build(t).print_result()
            # t.set_error_msg(CS.SUCCESS, "CHECKING")
            # dol(t, "check").build(t).run()

    def view(self):
        ret: Dict[str, List[TaskCfg]] = defaultdict(list)
        ct = defaultdict(int)
        tasks2 = query_task()
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
        logger.info(dict(ct))

    def exec(self, state=""):
        tasks: List[TaskCfg] = []
        tasks2 = query_task(self.key, state=state)
        for f in tasks2:

            f.check()
            # s, b, *args = f.error_msg.get_value().split(":")
            # if s == CS.FAILED:
            #     f.set_error_msg(CS.RUN, "WAIT")
            #     tasks.append(f)

        # owner, task_id, repo, pr = get_info_by_name(f.name)

    def query(self, key):
        for t in query_task(key):
            logger.info(t)

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
E       ModuleNotFoundError: No module named 'snowflake'

""".replace(
            "\n", ""
        )
        for f in query_task(self.key):
            if f.error_msg.get_value().startswith(CS.RUN):
                continue
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
