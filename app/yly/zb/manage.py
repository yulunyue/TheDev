from common.util.export import ToolBase,logger,File
from .util import WT


class ZbMangae(ToolBase):
    def query(self):
        WT.start()
    def dev(self):
        r=File("../../downloads")
        for f in r.list_dir():
            if not f.path.endswith(".zip"):
                continue
            name,pr=f.name.split("-")
            owner,task_id,repo_name=name.split("_")
            f.copy


if __name__ == "__main__":
    ZbMangae().run()
