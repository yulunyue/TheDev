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
from .util import INPUTS_DIR, TASK_DIR, get_info_by_name, INFO_DIR, TaskCfg, task_cfg

from .main import ZbTask


def query(key=""):
    fss = INFO_DIR.list_dir()
    ret: List[TaskCfg] = []
    for f in fss:
        c = task_cfg(f.name)
        if key and key not in c.id:
            continue
        ret.append(c)
    return ret


class ZbMangae(ToolBase):
    def submit(self):
        from .auto import WT

        WT.load().run()

    def clear(self, key=""):
        for t in query(key):
            t.zip_file.remove()

    def view(self, key=""):
        ret = defaultdict(list)
        for t in query(key):
            if t.zip_file.exists() or t.skip.get_value():
                continue
            ret[t.error_msg.get_value()].append(t.id)
        for k, tasks in ret.items():
            self.logger.debug(f"{k} {len(tasks)} {tasks}")

    def main(self, key="", docker_name=None):
        for f in query(key):
            t = ZbTask().prepare(f.key)
            t.main()
            t.exit()
        # owner, task_id, repo, pr = get_info_by_name(f.name)


if __name__ == "__main__":
    ZbMangae().run()
