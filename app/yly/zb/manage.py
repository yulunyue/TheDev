from common.util.export import ToolBase, logger, File, os, LOGER_PREFIX
from common.tool.export import OsUtil
from .util import TB, INPUTS_DIR, TASK_DIR, get_info_by_name
from .auto import WT
from .main import ZbTask


class ZbMangae(ToolBase):
    def web_run(self):
        c = WT.load()
        c.play(c.get_job_info)

    def dev(self):
        r = File("../../downloads")
        for f in r.list_dir():
            if not f.path.endswith(".zip"):
                continue

    def main(self, key=""):
        def ft(f: File):
            return key in f.name and f.path.endswith(".zip")

        fps = TASK_DIR.list_dir(-1, filter=ft)
        for f in fps:
            f.unzip(False)
            t = ZbTask()
            t.prepare(f.path.replace(".zip", ""))
            t.set_docker_image_name("zb:latest")

            t.main()
            t.exit()
            # owner, task_id, repo, pr = get_info_by_name(f.name)
        TB.save()


if __name__ == "__main__":
    ZbMangae().run()
