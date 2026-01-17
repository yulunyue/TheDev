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
    ThreadManage,
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
        f.input_dir.child(f"docker.log").path,
    )


class ZbMangae:

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

    def view(self):
        ret: Dict[str, List[TaskCfg]] = defaultdict(list)
        ct = defaultdict(int)
        tasks2 = query_task()
        for t in tasks2:
            test_ct, code_ct = t.get_result("test"), t.get_result("code")
            key = t.error_msg.get_value().split("=")[0]
            start_idx = key.find(":")
            if start_idx == -1:
                raise Exception(t, key)
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

    def run_all(self, key):
        tasks2 = [d for d in query_task(key) if d.check]
        # for t in tasks2:
        #     self.run_one(t)
        ThreadManage(max_workers=1).run(self.run_one, tasks2)

    def run_one(self, t):
        if isinstance(t, str):
            t = query_one(t)

        d = dol(t).build(t).load()
        d.run()

    def show_all(self, key, name):
        for d in query_task(key):
            self.show(d, name)

    def show(self, tk, name):
        t = dol(tk).build(tk).load()
        if name == "test":
            t.apply_test()
        elif name == "code":
            t.apply_code()
        else:
            t.rest_repo()
        t.print_result()
        t.save()
        t.make_launch_json()
        logger.info(t.get_py_test_main_code())
        # t.docker_build()
        vv = t.get_volumn_v(
            {
                t.local_repo.get_abs_path(): t.local_repo.path,
            }
        )
        logger.info(f"docker run -p 5678:5678 {vv} -it {t.docker_image_name}")
        logger.info(
            f"python -m debugpy --listen 0.0.0.0:5678 --wait-for-client py_test_main.py"
        )

    def query_log(self, key, search_key, log_name, util=""):
        for f in query_task(key):
            if not f.check():
                continue
            test_log = f.input_dir.child(log_name)
            if not test_log.exists():
                continue
            datas = test_log.read_file()
            idx = datas.find(search_key)
            if idx != -1:
                if util == CS.SKIPPED:
                    f.set_error_msg(CS.SKIPPED)
                elif util.startswith("env "):
                    _, env = util.split(" ")
                    f.set_env(env)
                logger.info(f"{f}->{datas[idx:idx+100]}")
