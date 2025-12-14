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
from .util import INPUTS_DIR, TASK_DIR, get_info_by_name, INFO_DIR, TaskCfg

from .main import ZbTask


def query(key=""):
    fss = INFO_DIR.list_dir()
    ret: List[ZbTask] = []
    for f in fss:
        t = ZbTask().prepare(f.name)
        if key and key not in t.local_cfg.name.get_value():
            continue
        ret.append(t)
    return ret


class ZbMangae(ToolBase):
    def submit(self):
        from .auto import WT

        WT.load().run()

    def view(self, key=""):
        ret = defaultdict(list)
        for t in query(key):
            if t.zip_file.exists():
                continue
            ret[t.local_cfg.error_msg.get_value()].append(t.task_id)
        for k, tasks in ret.items():
            self.logger.debug(f"{k} {len(tasks)} {tasks}")

    def main(self, key="", docker_name=None):
        for t in query(key):

            t.main()
            t.exit()
        # owner, task_id, repo, pr = get_info_by_name(f.name)


if __name__ == "__main__":
    ZbMangae().run()
