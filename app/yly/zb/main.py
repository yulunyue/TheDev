from common.util.export import (
    ToolBase,
    logger,
    File,
    os,
    LOGER_PREFIX,
    List,
    defaultdict,
)
from common.tool.export import OsUtil
from .util import (
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
)

from .zb_task import ZbTask


class ZbMangae(ToolBase):
    def submit(self):
        from .auto import WT

        WT.load().run()

    def clear(self, key=DEFAULT_REPO):
        for t in query_task(key):
            if t.zip_file.exists():
                logger.info(f"remove {t.zip_file}")
                t.zip_file.remove()

    def view(self, key=DEFAULT_REPO):
        ret = defaultdict(list)
        for t in query_task(key):
            if t.zip_file.exists():
                continue
            key = "NEEDMAKE: " if not t.zip_file.exists() else "NO_NEED: "
            key += t.error_msg.get_value()
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

    def test(self, key=DEFAULT_REPO, tp="docker_ignore"):
        for f in query_task(key):
            t = ZbTask().build(f)
            logger.run_capture_error(t.run, tp, captures=CS.ZB_TASK_FAIL)
        # owner, task_id, repo, pr = get_info_by_name(f.name)

    def rebuild(self, key="6036"):
        z = ZbTask().build(task_cfg(key))
        z.init()
        z.dock_util.re_build(z.input_dir.get_abs_path())

    def dev(self):
        pass


if __name__ == "__main__":
    ZbMangae().run()
