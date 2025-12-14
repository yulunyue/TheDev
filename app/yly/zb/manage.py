from common.util.export import ToolBase, logger, File, os, LOGER_PREFIX
from common.tool.export import OsUtil
from .util import INPUTS_DIR, TASK_DIR, get_info_by_name, INFO_DIR

from .main import ZbTask


class ZbMangae(ToolBase):
    def submit(self):
        from .auto import WT

        WT.load().run()

    def main(self, key="", docker_name=None):

        fps = INFO_DIR.list_dir()
        for f in fps:
            t = ZbTask()
            t.prepare(f.name)
            if key and key not in t.local_cfg.name.get_value():
                continue
            # if docker_name is None:
            #     pass
            t.main()
            t.exit()
            # owner, task_id, repo, pr = get_info_by_name(f.name)


if __name__ == "__main__":
    ZbMangae().run()
